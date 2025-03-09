import secrets
from collections import defaultdict
from dataclasses import fields
from typing import TYPE_CHECKING, Any, Optional, Type, TypeVar

import bcrypt
from apischema import deserialize
from fastapi import HTTPException, Request, status
from fastapi.openapi.models import OAuthFlowPassword, OAuthFlows
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param

if TYPE_CHECKING:
    from .model import T

_config_fields: dict[Type, Optional[Any]] = {}

Cls = TypeVar("Cls", bound=Type)

TOKEN_KEY_NAME = "access_token"


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[dict[str, str]] = None,
        auto_error: bool = True,
        token_key_name: str = TOKEN_KEY_NAME,
    ):
        self.token_key_name = token_key_name
        if not scopes:
            scopes = {}
        flows = OAuthFlows(password=OAuthFlowPassword(tokenUrl=tokenUrl, scopes=scopes))
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.cookies.get(self.token_key_name) or request.headers.get(
            "Authorization"
        )

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


class ConfigurationField:
    def __init__(self, name: str):
        self.name = name

    def __get__(self, instance, owner):
        assert instance is None
        try:
            return getattr(_config_fields[owner], self.name)
        except AttributeError:
            raise RuntimeError("Configuration not loaded") from None
        except KeyError:
            raise RuntimeError("Configuration is not root") from None


def load_configuration(cls: Cls) -> Cls:
    for field_ in fields(cls):
        setattr(cls, field_.name, ConfigurationField(field_.name))
    _config_fields[cls] = None
    return cls


def load_configuration_data(config: dict[str, Any]) -> None:
    for key, _ in _config_fields.items():
        _config_fields[key] = deserialize(key, config)


def idun(prefix: str, nbytes: int = 16) -> str:
    return f"{prefix}-{secrets.token_hex(nbytes)}"


def generate_password_hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_password_hash(hashed_password: bytes, input_password: str) -> bool:
    return bcrypt.checkpw(input_password.encode("utf-8"), hashed_password)


# Helper function for error handling
def ensure_user_owns_resource(current_account_id: str, resource_owner_id: str) -> None:
    """Raise an exception if the current account does not own the resource."""
    if current_account_id != resource_owner_id:
        raise Exception("You do not have permission to access this resource.")


def handle_update_files(files: list[dict[str, Any]], model: Type["T"]) -> list["T"]:
    categories = defaultdict(list)
    for item in files:
        categories[item["category"]].append(item)

    filtered_data = []
    for _, items in categories.items():
        without_id = [item for item in items if "id" not in item]
        with_id = [item for item in items if "id" in item]

        if without_id:
            filtered_data.append(model(**without_id[-1]))
            if with_id:
                [model.get(id=f["id"]).delete() for f in with_id]
        else:
            filtered_data.extend([model.get(id=f["id"]) for f in with_id])

    return filtered_data


def handle_update_resources(
    new_resources: list[dict[str, Any]], old_resources: list["T"], model: Type["T"]
) -> list["T"]:
    old_resource_ids = {sn.id for sn in old_resources}
    new_resource_ids = {sn["id"] for sn in new_resources if "id" in sn}

    resource_ids_to_delete = old_resource_ids - new_resource_ids
    resource_ids_to_create = [sn for sn in new_resources if "id" not in sn]

    [model.get(id=id).delete() for id in resource_ids_to_delete]

    return [model(**sn) for sn in resource_ids_to_create] + [
        model.get(id=id) for id in new_resource_ids
    ]


def remove_duplicates(list_objects: list, key: str) -> list:
    """Remove duplicate items in a list of objects based on given key."""
    if isinstance(list_objects[0], dict):
        uniques = {el[key]: el for el in list_objects}
    else:
        uniques = {getattr(el, key): el for el in list_objects}
    return list(uniques.values())


def to_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    try:
        return list(value)
    except TypeError:
        return [value]
