from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..errors import NoActivityFound
from ..utils import idun
from .base import Base
from .event import Event
from .resource import Resource


class Activity(Base, Resource):
    __tablename__ = "activity"
    __errors__ = {"_error": NoActivityFound}

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: idun("activity"))

    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    event_id: Mapped[str] = mapped_column(ForeignKey("event.id"))

    # relationships
    event: Mapped["Event"] = relationship("Event", back_populates="activities")
