from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..utils import idv2
from .base import Base
from .event import Event
from .resources import Resource


class File(Base, Resource):

    __tablename__ = "file"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: idv2("event", version=1)
    )

    path: Mapped[str] = mapped_column(String, nullable=False)

    # relationship

    # Many-to-Many relationship with Event
    events: Mapped[list["Event"]] = relationship(
        "Event",
        secondary="event_file",
        back_populates="files",
    )
