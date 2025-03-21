from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..errors import NoEventFound
from ..utils import idun
from .base import Base
from .entity import Entity

if TYPE_CHECKING:
    from .account import Account
    from .activity import Activity
    from .file import File
    from .tag import Tag
    from .ticket import Ticket


# TODO confirm the types and use them in react CategoryEvents
class EventCategory(Enum):
    COURSE = "course"
    CINEMA = "cinema"
    CONCERT = "concert"
    PARTY = "party"
    EXPOSITION = "exposition"
    LANGUAGE_EXCHANGE = "language_exchange"
    THEATER = "theater"
    GASTRONOMY = "gastronomy"
    DANCE = "dance"


class EventFrequency(Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class Event(Base, Entity):
    __tablename__ = "event"
    __errors__ = {"_error": NoEventFound}

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: idun("event"))

    category: Mapped[EventCategory] = mapped_column(SQLAEnum(EventCategory), nullable=False)

    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    frequency: Mapped[EventFrequency] = mapped_column(SQLAEnum(EventFrequency), nullable=False)

    # DONE add change name attr to title ? No
    # DONE add tags, another table or a list of strings ? yes table
    # DONE add artists, is it an accounts list with type artists ? no, it's a business
    # DONE add location: str ? latitude, longitude and city can be taken from location ?
    # DONE Add date: datetime or start_date and end_date ?
    # TODO Add interesados, participates ? is a number ?
    # DONE Add url or urls ? in Entity class ? yes and yes
    # TODO Add progrmacion table -> time and name and picture ?
    # TODO Add artists from Business model -> a relationship with Business filtering by artists ?

    # foreign key

    account_id: Mapped[str] = mapped_column(ForeignKey("account.id"), nullable=False)

    # relationships

    # One-to-Many relationships
    account: Mapped["Account"] = relationship("Account", back_populates="events")

    activities: Mapped[list["Activity"]] = relationship(
        "Activity", back_populates="event", cascade="all, delete-orphan"
    )

    files: Mapped[list["File"]] = relationship(
        "File", back_populates="event", cascade="all, delete-orphan"
    )

    tickets: Mapped[list["Ticket"]] = relationship(
        "Ticket", back_populates="event", cascade="all, delete-orphan"
    )

    # Many-to-Many relationships
    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="event_tag",
        back_populates="events",
    )
