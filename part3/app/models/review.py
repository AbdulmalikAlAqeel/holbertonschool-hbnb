"""Review model."""

from sqlalchemy.orm import validates

from app.extensions import db
from app.models.base import BaseModel
from app.models.user import User


class Review(BaseModel):
    """Represent a review for a place."""

    __tablename__ = "reviews"

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(
        db.String(36),
        db.ForeignKey("places.id"),
        nullable=False
    )
    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False
    )

    place = db.relationship("Place", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")

    def __init__(self, text, rating, place, user):
        """Initialize a review."""
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @validates("text")
    def validate_text(self, key, value):
        """Validate and set the review text."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Review text must be a non-empty string.")

        return value

    @validates("rating")
    def validate_rating(self, key, value):
        """Validate and set the review rating."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(
                "Rating must be an integer between 1 and 5."
            )

        if not 1 <= value <= 5:
            raise ValueError(
                "Rating must be an integer between 1 and 5."
            )

        return value

    @validates("place")
    def validate_place(self, key, value):
        """Validate the related place."""
        from app.models.place import Place

        if not isinstance(value, Place):
            raise ValueError("Place must be a Place instance.")

        return value

    @validates("user")
    def validate_user(self, key, value):
        """Validate the related user."""
        if not isinstance(value, User):
            raise ValueError("User must be a User instance.")

        return value
