from sqlalchemy import Boolean, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from .resource import Resource


class Entity(Resource):
    """
    Entity model for managing geographical and contact information.
    Extends the Resource base class.
    """

    # General information
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str | None] = mapped_column(String)
    phone: Mapped[str | None] = mapped_column(String)

    # Address details
    address: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    municipality: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    postcode: Mapped[str] = mapped_column(String, nullable=False)
    region: Mapped[str] = mapped_column(String, nullable=False)

    # Geographical coordinates
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    # Visibility
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    urls: Mapped[list[str] | None] = mapped_column(String, nullable=True, default=[])

    # DONE email
    # DONE phone number
    # DONE Add countty, municipality, postcode, region
