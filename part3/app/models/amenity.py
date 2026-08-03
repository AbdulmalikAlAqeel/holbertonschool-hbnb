from app.models.base import BaseModel

class Amenity(BaseModel):
    """Represents an amenity available at a Place (e.g., Wi-Fi, Pool)."""
    
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name must be a non-empty string.")
        self.name = name
