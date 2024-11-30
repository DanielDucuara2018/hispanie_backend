from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, LargeBinary, String, func
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..utils import generate_password_hash, idv2
from .base import Base
from .event import Event


class AccountType(Enum):
    USER = "user"
    ADMIN = "admin"


class Account(Base):

    __tablename__ = "account"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: idv2("account", version=1)
    )

    username: Mapped[str] = mapped_column(String, nullable=False)

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    type: Mapped[AccountType] = mapped_column(SQLAEnum(AccountType), nullable=False)

    _password: Mapped[bytes] = mapped_column("password", LargeBinary, nullable=False)

    creation_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )

    update_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=func.now()
    )

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
