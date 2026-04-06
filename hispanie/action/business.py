from typing import overload

from hispanie.action.account import read as read_accounts
from hispanie.action.tag import read as read_tags
from hispanie.config import logging
from hispanie.model import Business, File, SocialNetwork
from hispanie.schema import BusinessCreateRequest, BusinessUpdateRequest
from hispanie.utils import ensure_user_owns_resource, handle_update_files, handle_update_resources

logger = logging.getLogger(__name__)


async def create(business_data: BusinessCreateRequest, account_id: str) -> Business:
    account = await read_accounts(account_id)
    data = business_data.model_dump()
    logger.info("Adding new business: %s", data)
    social_networks = [SocialNetwork(**sn) for sn in data.pop("social_networks")]
    files = [await File(**file).create() for file in data.pop("files")]
    tags = await read_tags(id=[t["id"] for t in data.pop("tags")])
    business = await Business(
        account=account,
        files=files,
        social_networks=social_networks,
        tags=tags,
        **data,
    ).create()
    logger.info("Added new business %s", business.id)
    return business


@overload
async def read(business_id: str) -> Business: ...
@overload
async def read(**kwargs) -> list[Business]: ...
async def read(business_id: str | None = None, **kwargs) -> Business | list[Business]:
    if business_id:
        logger.info("Reading business: %s", business_id)
        return await Business.get(id=business_id)
    else:
        logger.info("Reading all business")
        return await Business.find(**kwargs)


async def update(
    business_id: str, account_id: str, business_data: BusinessUpdateRequest
) -> Business:
    business = await Business.get(id=business_id)
    ensure_user_owns_resource(account_id, business.account_id)
    data = business_data.model_dump(exclude_none=True)
    logger.info("Updating business: %s with %s", business_id, data)
    if tags := data.pop("tags", []):
        data["tags"] = await read_tags(id=[t["id"] for t in tags])
    if files := data.pop("files", []):
        data["files"] = await handle_update_files(files, File)
    if social_networks := data.pop("social_networks", []):
        data["social_networks"] = await handle_update_resources(
            social_networks, business.social_networks, SocialNetwork
        )
    result = await business.update(**data)
    logger.info("Updated business: %s", business_id)
    return result


async def delete(event_id: str, account_id: str) -> Business:
    logger.info("Deleting business: %s", event_id)
    business = await Business.get(id=event_id)
    ensure_user_owns_resource(account_id, business.account_id)
    result = await business.delete()
    logger.info("Deleted business: %s", event_id)
    return result
