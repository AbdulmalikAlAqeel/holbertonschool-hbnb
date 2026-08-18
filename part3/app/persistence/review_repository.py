"""Review-specific SQLAlchemy repository."""

from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    """Handle database operations specific to Review."""

    def __init__(self):
        """Initialize the repository for Review."""
        super().__init__(Review)
