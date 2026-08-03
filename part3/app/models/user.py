import re

from app.models.base import BaseModel


class User(BaseModel):
    """Represent a user profile in the system."""

    def __init__(
        self,
        email,
        first_name,
        last_name,
        password=None,
        is_admin=False
    ):
        """Initialize a user."""
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_admin = is_admin

    @property
    def email(self):
        """Return the user's email."""
        return self._email

    @email.setter
    def email(self, value):
        """Validate and set the user's email."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Email must be a non-empty string.")

        pattern = r"^[\w.-]+@[\w.-]+\.\w+$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format.")

        self._email = value

    @property
    def first_name(self):
        """Return the user's first name."""
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """Validate and set the user's first name."""
        self._first_name = self.validate_name(value, "First name")

    @property
    def last_name(self):
        """Return the user's last name."""
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """Validate and set the user's last name."""
        self._last_name = self.validate_name(value, "Last name")

    @property
    def is_admin(self):
        """Return whether the user is an administrator."""
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        """Validate and set administrator status."""
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean.")

        self._is_admin = value

    @staticmethod
    def validate_name(value, field_name):
        """Validate a user's first or last name."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{field_name} must be a non-empty string."
            )

        if len(value) > 50:
            raise ValueError(
                f"{field_name} must not exceed 50 characters."
            )

        return value
