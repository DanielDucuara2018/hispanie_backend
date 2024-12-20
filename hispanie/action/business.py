import logging

from ..model import Business
from ..schema import BusinessCreateRequest, BusinessUpdateRequest
from .account import read as read_accounts

logger = logging.getLogger(__name__)


# Helper function for error handling
def ensure_user_owns_event(current_account_id: int, event_owner_id: int) -> None:
    """
    Raise an exception if the current account does not own the business.
    """
    if current_account_id != event_owner_id:
        raise Exception("You do not have permission to access this business.")


def create(business_data: BusinessCreateRequest, account_id: str) -> Business:
    logger.info("Adding new business %s", business_data)
    account = read_accounts(account_id)
    business = Business(account=account, **business_data.model_dump()).create()
    logger.info("Added new business %s", business.id)
    return business


def read(business_id: str | None = None, **kwargs) -> Business | list[Business]:
    if business_id:
        logger.info("Reading %s data", business_id)
        result = Business.get(id=business_id)
    else:
        logger.info("Reading all data")
        result = Business.find(**kwargs)
    return result


def update(business_id: str, account_id: str, business_data: BusinessUpdateRequest) -> Business:
    logger.info("Updating %s business", business_id)
    business = Business.get(id=business_id)
    ensure_user_owns_event(account_id, business.account_id)
    result = business.update(**business_data.model_dump(exclude_none=True))
    logger.info("Updated business %s", business_id)
    return result


def delete(event_id: str, account_id: str) -> Business:
    logger.info("Deleting %s business", event_id)
    business = Business.get(id=event_id)
    ensure_user_owns_event(account_id, business.account_id)
    result = business.delete()
    logger.info("Deleted business %s", event_id)
    return result
