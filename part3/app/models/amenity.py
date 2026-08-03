from app.models.base import BaseModel


class Amenity(BaseModel):
    """Represent an amenity available at a place."""

    def __init__(self, name):
        """Initialize an amenity."""
        super().__init__()
        self.name = name

    @property
    def name(self):
        """Return the amenity name."""
        return self._name

    @name.setter
    def name(self, value):
        """Validate and set the amenity name."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                "Amenity name must be a non-empty string."
            )

        if len(value) > 50:
            raise ValueError(
                "Amenity name must not exceed 50 characters."
            )

        self._name = value
