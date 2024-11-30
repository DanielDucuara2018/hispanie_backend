from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, func
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..utils import idv2
from .base import Base

if TYPE_CHECKING:
    from .account import Account


# Enum for Event Types TODO define the type
class EventCategory(Enum):
    CONFERENCE = "conference"
    WORKSHOP = "workshop"
    MEETUP = "meetup"
    FESTIVAL = "festival"


class Event(Base):
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

    creation_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )

    update_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=func.now()
    )

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)

    account: Mapped["Account"] = relationship("Account", back_populates="events")
