from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .resources import Resource


# Association Class for Many-to-Many relationship
class EventFile(Base, Resource):
    __tablename__ = "event_file"

    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), primary_key=True)

    file_id: Mapped[int] = mapped_column(ForeignKey("file.id"), primary_key=True)
