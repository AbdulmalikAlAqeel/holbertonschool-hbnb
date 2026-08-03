import uuid
from datetime import datetime


class BaseModel:
    """Define common attributes and methods for domain models."""

    def __init__(self):
        """Initialize an object with UUID and timestamps."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the modification timestamp."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update allowed attributes using values from a dictionary."""
        if not isinstance(data, dict):
            raise ValueError("Update data must be a dictionary.")

        protected_keys = {"id", "created_at", "updated_at"}

        for key, value in data.items():
            if key not in protected_keys and hasattr(self, key):
                setattr(self, key, value)

        self.save()
