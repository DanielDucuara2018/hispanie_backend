import logging
from typing import overload

from ..model import Activity, Event
from ..schema import ActivityCreateRequest, ActivityUpdateRequest

logger = logging.getLogger(__name__)


def create(activity_data: ActivityCreateRequest) -> Activity:
    # Check event
    Event.get(id=activity_data.event_id)

    if activities := read(event_id=activity_data.event_id, name=activity_data.name):
        logger.info("Activity already exists: %s", activities[0].id)
        return activities[0]

    logger.info("Adding new activity: %s", activity_data)
    activity = Activity(**activity_data.model_dump()).create()
    logger.info("Added new activity: %s", activity.id)
    return activity


@overload
def read(activity_id: str) -> Activity: ...
@overload
def read(**kwargs) -> list[Activity]: ...
def read(activity_id: str | None = None, **kwargs) -> Activity | list[Activity]:
    if activity_id:
        logger.info("Reading activity: %s", activity_id)
        return Activity.get(id=activity_id)
    else:
        logger.info("Reading all activities with filters %s", kwargs)
        return Activity.find(**kwargs)


def update(activity_id: str, activity_data: ActivityUpdateRequest) -> Activity:
    logger.info("Updating activity: %s with %s", activity_id, activity_data)
    tag = Activity.get(id=activity_id)
    result = tag.update(**activity_data.model_dump(exclude_none=True))
    logger.info("Updated activity: %s", activity_id)
    return result


def delete(activity_id: str) -> Activity:
    logger.info("Deleting activity: %s", activity_id)
    activity = Activity.get(id=activity_id)
    result = activity.delete()
    logger.info("Deleted activity: %s", activity_id)
    return result
