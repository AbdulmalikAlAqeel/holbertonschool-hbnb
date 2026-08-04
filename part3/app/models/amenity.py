from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name="", **kwargs):
        super().__init__(**kwargs)
        self.name = name  # Triggers property setter validation automatically

    @property
    def name(self):
        """Return the amenity name."""
        return self._name

    @name.setter
    def name(self, value):
        """Validate and set the amenity name."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Amenity name is required and cannot be empty.")

        if len(value) > 50:
            raise ValueError("Amenity name must not exceed 50 characters.")

        self._name = value.strip()

    def update(self, data):
        """Update amenity attributes dynamically using property setters."""
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue

            if hasattr(self, key):
                setattr(self, key, value)  # Triggers @name.setter validation

        if hasattr(super(), 'save'):
            super().save()
