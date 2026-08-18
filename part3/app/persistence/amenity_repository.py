"""Amenity-specific SQLAlchemy repository."""

from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    """Handle database operations specific to Amenity."""

    def __init__(self):
        """Initialize the repository for Amenity."""
        super().__init__(Amenity)
