"""User model."""

import re

from app.extensions import bcrypt, db
from app.models.base import BaseModel


class User(BaseModel):
    """Represent a user profile in the system."""

    __tablename__ = "users"

    _first_name = db.Column(
        "first_name",
        db.String(50),
        nullable=False
    )
    _last_name = db.Column(
        "last_name",
        db.String(50),
        nullable=False
    )
    _email = db.Column(
        "email",
        db.String(120),
        nullable=False,
        unique=True
    )
    password = db.Column(
        db.String(128),
        nullable=False
    )
    _is_admin = db.Column(
        "is_admin",
        db.Boolean,
        default=False,
        nullable=False
    )

    places = db.relationship(
        "Place",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
    reviews = db.relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __init__(
        self,
        first_name="",
        last_name="",
        email="",
        password=None,
        is_admin=False
    ):
        """Initialize a user."""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        if password is not None:
            self.hash_password(password)

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
        self._first_name = self.validate_name(
            value,
            "First name"
        )

    @property
    def last_name(self):
        """Return the user's last name."""
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """Validate and set the user's last name."""
        self._last_name = self.validate_name(
            value,
            "Last name"
        )

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

    def hash_password(self, password):
        """Hash and store a plaintext password."""
        if not isinstance(password, str) or not password:
            raise ValueError(
                "Password must be a non-empty string."
            )

        self.password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def verify_password(self, password):
        """Check a plaintext password against its stored hash."""
        if not self.password:
            return False

        return bcrypt.check_password_hash(
            self.password,
            password
        )

    def update(self, data):
        """Update allowed user attributes."""
        if not isinstance(data, dict):
            raise ValueError(
                "Update data must be a dictionary."
            )

        protected_keys = {
            "id",
            "created_at",
            "updated_at",
            "is_admin"
        }

        for key, value in data.items():
            if key in protected_keys:
                continue

            if key == "password":
                self.hash_password(value)
            elif hasattr(self, key):
                setattr(self, key, value)

        self.save()
