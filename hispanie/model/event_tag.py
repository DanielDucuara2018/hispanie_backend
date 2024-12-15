from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .resource import Resource


# Association Class for Many-to-Many relationship
class EventTag(Base, Resource):
    __tablename__ = "event_tag"

    event_id: Mapped[str] = mapped_column(ForeignKey("event.id"), primary_key=True)

    tag_id: Mapped[str] = mapped_column(ForeignKey("tag.id"), primary_key=True)
