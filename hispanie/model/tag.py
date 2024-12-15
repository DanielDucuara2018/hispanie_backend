from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..utils import idv2
from .base import Base
from .business import Business
from .event import Event
from .resource import Resource


class Tag(Base, Resource):

    __tablename__ = "tag"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: idv2("tag", version=1)
    )

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    # relationship

    # Many-to-Many relationship with Event
    events: Mapped[list["Event"]] = relationship(
        "Event",
        secondary="event_tag",
        back_populates="tags",
    )

    # Many-to-Many relationship with Business
    businesses: Mapped[list["Business"]] = relationship(
        "Business",
        secondary="business_tag",
        back_populates="tags",
    )
