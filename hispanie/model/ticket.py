from enum import Enum

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..errors import NoTicketFound
from ..utils import idun
from .base import Base
from .event import Event
from .resource import Resource


class Currency(Enum):
    AED = "AED"
    COP = "COP"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    PEN = "PEN"
    QAR = "QAR"
    USD = "USD"


class Ticket(Base, Resource):
    __tablename__ = "ticket"
    __errors__ = {"_error": NoTicketFound}

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: idun("ticket"))

    name: Mapped[str] = mapped_column(nullable=False)

    cost: Mapped[float] = mapped_column(default=0.0, nullable=False)

    currency: Mapped[Currency] = mapped_column(nullable=False)

    event_id: Mapped[str] = mapped_column(ForeignKey("event.id"))

    __table_args__ = (UniqueConstraint("event_id", "name", name="unique_ticket_name_for_event"),)

    # relationships
    event: Mapped["Event"] = relationship("Event", back_populates="tickets")
