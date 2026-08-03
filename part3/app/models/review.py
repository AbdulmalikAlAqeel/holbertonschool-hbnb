from app.models.base import BaseModel
from app.models.user import User


class Review(BaseModel):
    """Represent a review for a place."""

    def __init__(self, text, rating, place, user):
        """Initialize a review."""
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        """Return the review text."""
        return self._text

    @text.setter
    def text(self, value):
        """Validate and set the review text."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Review text must be a non-empty string.")

        self._text = value

    @property
    def rating(self):
        """Return the review rating."""
        return self._rating

    @rating.setter
    def rating(self, value):
        """Validate and set the review rating."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(
                "Rating must be an integer between 1 and 5."
            )

        if not 1 <= value <= 5:
            raise ValueError(
                "Rating must be an integer between 1 and 5."
            )

        self._rating = value

    @property
    def place(self):
        """Return the related Place object."""
        return self._place

    @place.setter
    def place(self, value):
        """Validate and set the related place."""
        from app.models.place import Place

        if not isinstance(value, Place):
            raise ValueError("Place must be a Place instance.")

        self._place = value

    @property
    def user(self):
        """Return the related User object."""
        return self._user

    @user.setter
    def user(self, value):
        """Validate and set the related user."""
        if not isinstance(value, User):
            raise ValueError("User must be a User instance.")

        self._user = value

    @property
    def place_id(self):
        """Return the place ID for API compatibility."""
        return self.place.id

    @property
    def user_id(self):
        """Return the user ID for API compatibility."""
        return self.user.id
