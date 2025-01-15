import logging

from ..model import Tag
from ..schema import TagCreateRequest, TagUpdateRequest

logger = logging.getLogger(__name__)


def create(account_id: str, tag_data: TagCreateRequest) -> Tag:
    logger.info("Adding new tag: %s", tag_data)
    tag = Tag(**tag_data.model_dump()).create()
    logger.info("Added new tag: %s", tag.id)
    return tag


def read(account_id: str, tag_id: str | None = None, **kwargs) -> Tag | list[Tag]:
    if tag_id:
        logger.info("Reading tag: %s", tag_id)
        return Tag.get(id=tag_id)
    else:
        logger.info("Reading all tags")
        return Tag.find(**kwargs)


def update(account_id: str, tag_id: str, tag_data: TagUpdateRequest) -> Tag:
    logger.info("Updating tag: %s with %s", tag_id, tag_data)
    tag = Tag.get(id=tag_id)
    result = tag.update(**tag_data.model_dump(exclude_none=True))
    logger.info("Updated tag: %s", tag_id)
    return result


def delete(account_id: str, tag_id: str) -> Tag:
    logger.info("Deleting tag: %s", tag_id)
    tag = Tag.get(id=tag_id)
    result = tag.delete()
    logger.info("Deleted tag: %s", tag_id)
    return result
