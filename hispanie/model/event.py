from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Float, ForeignKey, String
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..utils import idv2
from .base import Base
from .resources import Resource

if TYPE_CHECKING:
    from .account import Account
    from .file import File


# Enum for Event Types TODO define the type
class EventCategory(Enum):
    CONFERENCE = "conference"
    WORKSHOP = "workshop"
    MEETUP = "meetup"
    FESTIVAL = "festival"


class Event(Base, Resource):
    __tablename__ = "event"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: idv2("event", version=1)
    )

    name: Mapped[str] = mapped_column(String, nullable=False)

    city: Mapped[str] = mapped_column(String, nullable=False)

    latitude: Mapped[float] = mapped_column(Float, nullable=False)

    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    type: Mapped[EventCategory] = mapped_column(SQLAEnum(EventCategory), nullable=False)

    description: Mapped[str | None] = mapped_column(String, nullable=True)

    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # foreign key

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)

    # relationships

    account: Mapped["Account"] = relationship("Account", back_populates="events")

    # Many-to-Many relationship with File
    files: Mapped[list["File"]] = relationship(
        "File",
        secondary="event_file",
        back_populates="events",
    )
