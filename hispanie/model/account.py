from enum import Enum

from sqlalchemy import Enum as SQLAEnum
from sqlalchemy import LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..utils import generate_password_hash, idv2
from .base import Base
from .business import Business
from .event import Event
from .file import File
from .resource import Resource


class AccountType(Enum):
    USER = "user"
    ADMIN = "admin"


class Account(Base, Resource):
    """
    Represents an account in the system, managing user credentials, contact information, and related entities.

    Attributes:
        id (str): A unique identifier for the account, generated using the `idv2` utility.
        username (str): The username of the account holder. Uniqueness to be enforced.
        email (str): The email address associated with the account. Must be unique.
        phone (str | None): The phone number of the account holder, optional.
        type (AccountType): The type of account, either "user" or "admin".
        _password (bytes): The hashed password for the account, stored securely.

    Relationships:
        events (list[Event]): A list of events created by this account. Cascade delete enabled.
        businesses (list[Business]): A list of businesses associated with this account. Cascade delete enabled.
        files (list[File]): A list of files uploaded by this account. Cascade delete enabled.

    Properties:
        password (bytes): Getter for the hashed password.
        password (str): Setter for the password, which hashes the input string before storage.

    Notes:
        - Passwords are securely hashed using the `generate_password_hash` utility.
        - The `email` field is enforced as unique, and error handling for uniqueness violations is expected in application logic.
        - The `username` field's uniqueness should also be validated.
        - The `type` field categorizes the account as either a regular user or an admin.

    Usage:
        account = Account(username="johndoe", email="john@example.com", type=AccountType.USER)
        account.password = "securepassword123"  # Automatically hashes the password
    """

    __tablename__ = "account"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: idv2("account", version=1)
    )

    username: Mapped[str] = mapped_column(String, nullable=False)  # TODO is it unique ?

    email: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )  # TODO handle unique errors

    phone: Mapped[str] = mapped_column(String, nullable=True)

    type: Mapped[AccountType] = mapped_column(SQLAEnum(AccountType), nullable=False)

    _password: Mapped[bytes] = mapped_column("password", LargeBinary, nullable=False)

    # DONE Add profile image for accounts
    # DONE Add phone number ? Added
    # DONE Add artist type ? no
    # DONE Add name and surname ? no

    # relationships

    events: Mapped[list["Event"]] = relationship(
        "Event", back_populates="account", cascade="all, delete-orphan"
    )

    businesses: Mapped[list["Business"]] = relationship(
        "Business", back_populates="account", cascade="all, delete-orphan"
    )

    files: Mapped[list["File"]] = relationship(
        "File", back_populates="account", cascade="all, delete-orphan"
    )

    @property
    def password(self) -> bytes:
        """Getter for the hashed password."""
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        """Setter to hash and store the password."""
        self._password = generate_password_hash(value)
