from typing import overload

from ..config import logging
from ..model import Business, File, SocialNetwork
from ..schema import BusinessCreateRequest, BusinessUpdateRequest
from ..utils import ensure_user_owns_resource, handle_update_files, handle_update_resources
from .account import read as read_accounts
from .tag import read as read_tags

logger = logging.getLogger(__name__)


def create(business_data: BusinessCreateRequest, account_id: str) -> Business:
    account = read_accounts(account_id)
    data = business_data.model_dump()
    logger.info("Adding new business: %s", data)
    # Format and check extra models
    social_networks = [SocialNetwork(**sn) for sn in data.pop("social_networks")]
    files = [File(**file).create() for file in data.pop("files")]
    tags = read_tags(id=[t["id"] for t in data.pop("tags")])
    business = Business(
        account=account,
        files=files,
        social_networks=social_networks,
        tags=tags,
        **data,
    ).create()
    logger.info("Added new business %s", business.id)
    return business


@overload
def read(business_id: str) -> Business: ...
@overload
def read(**kwargs) -> list[Business]: ...
def read(business_id: str | None = None, **kwargs) -> Business | list[Business]:
    if business_id:
        logger.info("Reading business: %s", business_id)
        return Business.get(id=business_id)
    else:
        logger.info("Reading all business")
        return Business.find(**kwargs)


def update(business_id: str, account_id: str, business_data: BusinessUpdateRequest) -> Business:
    business = Business.get(id=business_id)
    ensure_user_owns_resource(account_id, business.account_id)
    data = business_data.model_dump(exclude_none=True)
    logger.info("Updating business: %s with %s", business_id, data)
    # Format and check tags
    if tags := data.pop("tags", []):
        data["tags"] = read_tags(id=[t["id"] for t in tags])
    if files := data.pop("files", []):
        data["files"] = handle_update_files(files, File)
    if social_networks := data.pop("social_networks", []):
        data["social_networks"] = handle_update_resources(
            social_networks, business.social_networks, SocialNetwork
        )
    result = business.update(**data)
    logger.info("Updated business: %s", business_id)
    return result


def delete(event_id: str, account_id: str) -> Business:
    logger.info("Deleting business: %s", event_id)
    business = Business.get(id=event_id)
    ensure_user_owns_resource(account_id, business.account_id)
    result = business.delete()
    logger.info("Deleted business: %s", event_id)
    return result
