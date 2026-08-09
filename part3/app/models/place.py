"""Place model."""

from sqlalchemy.orm import validates

from app.extensions import db
from app.models.base import BaseModel
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place_amenity import place_amenity


class Place(BaseModel):
    """Represent a rental place."""

    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False
    )

    owner = db.relationship("User", back_populates="places")
    reviews = db.relationship(
        "Review",
        back_populates="place",
        cascade="all, delete-orphan"
    )
    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        back_populates="places"
    )

    def __init__(
        self,
        title,
        description,
        price,
        latitude,
        longitude,
        owner
    ):
        """Initialize a place."""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

    @validates("title")
    def validate_title(self, key, value):
        """Validate and set the place title."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title must be a non-empty string.")

        if len(value) > 100:
            raise ValueError("Title must not exceed 100 characters.")

        return value

    @validates("description")
    def validate_description(self, key, value):
        """Validate and set the optional description."""
        if value is not None and not isinstance(value, str):
            raise ValueError("Description must be a string.")

        return value

    @validates("price")
    def validate_price(self, key, value):
        """Validate and set the place price."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("Price must be a positive number.")

        if value <= 0:
            raise ValueError("Price must be a positive number.")

        return float(value)

    @validates("latitude")
    def validate_latitude(self, key, value):
        """Validate and set the latitude."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("Latitude must be between -90.0 and 90.0.")

        if not -90.0 <= value <= 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0.")

        return float(value)

    @validates("longitude")
    def validate_longitude(self, key, value):
        """Validate and set the longitude."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(
                "Longitude must be between -180.0 and 180.0."
            )

        if not -180.0 <= value <= 180.0:
            raise ValueError(
                "Longitude must be between -180.0 and 180.0."
            )

        return float(value)

    @validates("owner")
    def validate_owner(self, key, value):
        """Validate the owner relationship."""
        if not isinstance(value, User):
            raise ValueError("Owner must be a User instance.")

        return value

    def add_amenity(self, amenity):
        """Associate an Amenity object with the place."""
        if not isinstance(amenity, Amenity):
            raise ValueError("Amenity must be an Amenity instance.")

        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    def add_review(self, review):
        """Associate a Review object with the place."""
        from app.models.review import Review

        if not isinstance(review, Review):
            raise ValueError("Review must be a Review instance.")

        if review.place is not self:
            raise ValueError("Review does not belong to this place.")

        if review not in self.reviews:
            self.reviews.append(review)
            self.save()
