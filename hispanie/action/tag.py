from typing import overload

from hispanie.config import logging
from hispanie.model import Tag
from hispanie.schema import TagCreateRequest, TagUpdateRequest

logger = logging.getLogger(__name__)


async def create(tag_data: TagCreateRequest) -> Tag:
    if tags := await read(name=tag_data.name):
        logger.info("Tag already exists: %s", tags[0].id)
        return tags[0]

    logger.info("Adding new tag: %s", tag_data)
    tag = await Tag(**tag_data.model_dump()).create()
    logger.info("Added new tag: %s", tag.id)
    return tag


@overload
async def read(tag_id: str) -> Tag: ...
@overload
async def read(**kwargs) -> list[Tag]: ...
async def read(tag_id: str | None = None, **kwargs) -> Tag | list[Tag]:
    if tag_id:
        logger.info("Reading tag: %s", tag_id)
        return await Tag.get(id=tag_id)
    else:
        logger.info("Reading all tags")
        return await Tag.find(**kwargs)


async def update(tag_id: str, tag_data: TagUpdateRequest) -> Tag:
    logger.info("Updating tag: %s with %s", tag_id, tag_data)
    tag = await Tag.get(id=tag_id)
    result = await tag.update(**tag_data.model_dump(exclude_none=True))
    logger.info("Updated tag: %s", tag_id)
    return result


async def delete(tag_id: str) -> Tag:
    logger.info("Deleting tag: %s", tag_id)
    tag = await Tag.get(id=tag_id)
    result = await tag.delete()
    logger.info("Deleted tag: %s", tag_id)
    return result
