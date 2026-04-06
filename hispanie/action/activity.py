from typing import overload

from hispanie.config import logging
from hispanie.model import Activity, Event
from hispanie.schema import ActivityCreateRequest, ActivityUpdateRequest

logger = logging.getLogger(__name__)


async def create(activity_data: ActivityCreateRequest) -> Activity:
    await Event.get(id=activity_data.event_id)

    if activities := await read(event_id=activity_data.event_id, name=activity_data.name):
        logger.info("Activity already exists: %s", activities[0].id)
        return activities[0]

    logger.info("Adding new activity: %s", activity_data)
    activity = await Activity(**activity_data.model_dump()).create()
    logger.info("Added new activity: %s", activity.id)
    return activity


@overload
async def read(activity_id: str) -> Activity: ...
@overload
async def read(**kwargs) -> list[Activity]: ...
async def read(activity_id: str | None = None, **kwargs) -> Activity | list[Activity]:
    if activity_id:
        logger.info("Reading activity: %s", activity_id)
        return await Activity.get(id=activity_id)
    else:
        logger.info("Reading all activities with filters %s", kwargs)
        return await Activity.find(**kwargs)


async def update(activity_id: str, activity_data: ActivityUpdateRequest) -> Activity:
    logger.info("Updating activity: %s with %s", activity_id, activity_data)
    tag = await Activity.get(id=activity_id)
    result = await tag.update(**activity_data.model_dump(exclude_none=True))
    logger.info("Updated activity: %s", activity_id)
    return result


async def delete(activity_id: str) -> Activity:
    logger.info("Deleting activity: %s", activity_id)
    activity = await Activity.get(id=activity_id)
    result = await activity.delete()
    logger.info("Deleted activity: %s", activity_id)
    return result
