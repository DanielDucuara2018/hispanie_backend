from enum import Enum

from sqlalchemy import Enum as SQLAEnum
from sqlalchemy import LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..utils import generate_password_hash, idv2
from .base import Base
from .event import Event
from .resources import Resource


class AccountType(Enum):
    USER = "user"
    ADMIN = "admin"


class Account(Base, Resource):

    __tablename__ = "account"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: idv2("account", version=1)
    )

    username: Mapped[str] = mapped_column(String, nullable=False)  # TODO is it unique ?

    email: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )  # TODO handle unique errors

    type: Mapped[AccountType] = mapped_column(SQLAEnum(AccountType), nullable=False)

    _password: Mapped[bytes] = mapped_column("password", LargeBinary, nullable=False)

    # relationships

    events: Mapped[list["Event"]] = relationship(
        "Event", back_populates="account", cascade="all, delete-orphan"
    )

    @property
    def password(self) -> bytes:
        """Getter for the hashed password."""
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        """Setter to hash and store the password."""
        self._password = generate_password_hash(value)
