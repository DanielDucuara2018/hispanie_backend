import random
from dataclasses import fields
from typing import Any, Optional, Type, TypeVar

import bcrypt
from apischema import deserialize
from fastapi import HTTPException, Request, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param

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
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
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


def idv2(prefix: str, *, version: int = 0, code: int = 1022) -> str:  # fix calculation
    random_bytes = (version << 127) + (code << 127) + random.getrandbits(117)
    return f"{prefix}-{random_bytes:032x}"


def generate_password_hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_password_hash(hashed_password: bytes, input_password: str) -> bool:
    return bcrypt.checkpw(input_password.encode("utf-8"), hashed_password)


# Helper function for error handling
def ensure_user_owns_resource(current_account_id: str, resource_owner_id: int) -> None:
    """
    Raise an exception if the current account does not own the resource.
    """
    if current_account_id != resource_owner_id:
        raise Exception("You do not have permission to access this resource.")


def to_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    try:
        return list(value)
    except TypeError:
        return [value]
