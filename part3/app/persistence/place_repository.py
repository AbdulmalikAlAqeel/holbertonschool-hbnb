"""Place-specific SQLAlchemy repository."""

from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    """Handle database operations specific to Place."""

    def __init__(self):
        """Initialize the repository for Place."""
        super().__init__(Place)
