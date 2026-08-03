from app.models.base import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


class Place(BaseModel):
    """Represent a rental place."""

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
        self.amenities = []
        self.reviews = []

    @property
    def title(self):
        """Return the place title."""
        return self._title

    @title.setter
    def title(self, value):
        """Validate and set the place title."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title must be a non-empty string.")

        if len(value) > 100:
            raise ValueError("Title must not exceed 100 characters.")

        self._title = value

    @property
    def description(self):
        """Return the place description."""
        return self._description

    @description.setter
    def description(self, value):
        """Validate and set the optional description."""
        if value is not None and not isinstance(value, str):
            raise ValueError("Description must be a string.")

        self._description = value

    @property
    def price(self):
        """Return the place price."""
        return self._price

    @price.setter
    def price(self, value):
        """Validate and set the place price."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("Price must be a positive number.")

        if value <= 0:
            raise ValueError("Price must be a positive number.")

        self._price = float(value)

    @property
    def latitude(self):
        """Return the place latitude."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Validate and set the latitude."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(
                "Latitude must be between -90.0 and 90.0."
            )

        if not -90.0 <= value <= 90.0:
            raise ValueError(
                "Latitude must be between -90.0 and 90.0."
            )

        self._latitude = float(value)

    @property
    def longitude(self):
        """Return the place longitude."""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Validate and set the longitude."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(
                "Longitude must be between -180.0 and 180.0."
            )

        if not -180.0 <= value <= 180.0:
            raise ValueError(
                "Longitude must be between -180.0 and 180.0."
            )

        self._longitude = float(value)

    @property
    def owner(self):
        """Return the owner object."""
        return self._owner

    @owner.setter
    def owner(self, value):
        """Validate and set the owner."""
        if not isinstance(value, User):
            raise ValueError("Owner must be a User instance.")

        self._owner = value

    @property
    def owner_id(self):
        """Return the owner ID for API compatibility."""
        return self.owner.id

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
