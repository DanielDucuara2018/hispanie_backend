from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..utils import idv2
from .base import Base
from .business import Business
from .event import Event
from .resource import Resource

if TYPE_CHECKING:
    from .account import Account


class File(Base, Resource):
    __tablename__ = "file"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: idv2("event", version=1)
    )

    path: Mapped[str] = mapped_column(String, nullable=False)

    # TODO Add a type to know where the file is gonna be shown ? ex: profile

    # foreign key
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))

    # relationship

    # Zero-to-Many relationship with account
    account: Mapped["Account"] = relationship("Account", back_populates="files")

    # Many-to-Many relationship with Event
    events: Mapped[list["Event"]] = relationship(
        "Event",
        secondary="event_file",
        back_populates="files",
    )

    # Many-to-Many relationship with Business
    businesses: Mapped[list["Business"]] = relationship(
        "Business",
        secondary="business_file",
        back_populates="files",
    )
