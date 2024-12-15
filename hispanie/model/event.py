from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..utils import idv2
from .base import Base
from .entity import Entity

if TYPE_CHECKING:
    from .account import Account
    from .file import File
    from .tag import Tag


# TODO confirm the types and use them in react CategoryEvents
class EventCategory(Enum):
    COURSE = "course"
    CINEMA = "cinema"
    CONCERT = "concert"
    PARTY = "party"
    # expositions
    # language exchange
    # teatro
    # gastronomy
    # Dance


class Event(Base, Entity):
    __tablename__ = "event"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: idv2("event", version=1)
    )

    category: Mapped[EventCategory] = mapped_column(SQLAEnum(EventCategory), nullable=False)

    price: Mapped[float] = mapped_column(Float, nullable=False)

    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # DONE add change name attr to title ? No
    # DONE add tags, another table or a list of strings ? yes table
    # DONE add artists, is it an accounts list with type artists ? no, it's a business
    # DONE add location: str ? latitude, longitude and city can be taken from location ?
    # DONE Add price: float
    # DONE Add date: datetime or start_date and end_date ?
    # TODO Add interesados, participates ? is a number ?
    # DONE Add url or urls ? in Entity class ? yes and yes
    # TODO Add progrmacion table -> time and name and picture ?

    # foreign key

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)

    # relationships

    # One-to-Many relationship with account
    account: Mapped["Account"] = relationship("Account", back_populates="events")

    # Many-to-Many relationship with File
    files: Mapped[list["File"]] = relationship(
        "File",
        secondary="event_file",
        back_populates="events",
    )

    # Many-to-Many relationship with Tag
    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="event_tag",
        back_populates="events",
    )
