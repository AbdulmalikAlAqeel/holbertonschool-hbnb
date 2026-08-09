"""Amenity model."""

from sqlalchemy.orm import validates

from app.extensions import db
from app.models.base import BaseModel
from app.models.place_amenity import place_amenity


class Amenity(BaseModel):
    """Represent an amenity that can be linked to places."""

    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False, unique=True)

    places = db.relationship(
        "Place",
        secondary=place_amenity,
        back_populates="amenities"
    )

    def __init__(self, name="", **kwargs):
        """Initialize an amenity."""
        super().__init__()
        self.name = name

    @validates("name")
    def validate_name(self, key, value):
        """Validate and set the amenity name."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                "Amenity name is required and cannot be empty."
            )

        if len(value) > 50:
            raise ValueError(
                "Amenity name must not exceed 50 characters."
            )

        return value.strip()
