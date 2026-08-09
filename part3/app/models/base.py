"""Base model for SQLAlchemy entities."""

import uuid
from datetime import datetime

from app.extensions import db


class BaseModel(db.Model):
    """Define common attributes and methods for database models."""

    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def __init__(self):
        """Initialize UUID and timestamps before persistence."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Return a dictionary representation of the model."""
        result = {
            'id': self.id,
            'created_at': (
                self.created_at.isoformat()
                if self.created_at else None
            ),
            'updated_at': (
                self.updated_at.isoformat()
                if self.updated_at else None
            )
        }

        for key, value in self.__dict__.items():
            if key.startswith('_sa_'):
                continue

            if key in {'id', 'created_at', 'updated_at'}:
                continue

            clean_key = key[1:] if key.startswith('_') else key

            if isinstance(value, list):
                result[clean_key] = [
                    item.id if hasattr(item, 'id') else item
                    for item in value
                ]
            elif hasattr(value, 'id'):
                result[clean_key] = value.id
            else:
                result[clean_key] = value

        return result

    def save(self):
        """Update the modification timestamp."""
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """Update allowed attributes using values from a dictionary."""
        if not isinstance(data, dict):
            raise ValueError("Update data must be a dictionary.")

        protected_keys = {"id", "created_at", "updated_at"}

        for key, value in data.items():
            if key not in protected_keys and hasattr(self, key):
                setattr(self, key, value)

        self.save()
