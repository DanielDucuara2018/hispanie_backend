from sqlalchemy import Boolean, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from .resource import Resource


class Entity(Resource):
    """Entity model for managing geographical and contact information."""

    # General information
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str | None] = mapped_column(String)
    phone: Mapped[str | None] = mapped_column(String)

    # Address details
    address: Mapped[str | None] = mapped_column(String)
    country: Mapped[str | None] = mapped_column(String)
    municipality: Mapped[str | None] = mapped_column(String)
    city: Mapped[str | None] = mapped_column(String)
    postcode: Mapped[str | None] = mapped_column(String)
    region: Mapped[str | None] = mapped_column(String)

    # Geographical coordinates
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)

    # Visibility
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # DONE email
    # DONE phone number
    # DONE Add countty, municipality, postcode, region
