from models.base_model import BaseModel

class Place(BaseModel):
    """Represents a rental listing/place in the system."""
    
    def __init__(self, title, description, price, latitude, longitude, owner_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = self.validate_title(title)
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner_id = owner_id  # Linked User ID
        self.amenities = []       # List of associated Amenity IDs
        self.reviews = []         # List of associated Review IDs

    @staticmethod
    def validate_title(title):
        if not title or not isinstance(title, str):
            raise ValueError("Title must be a non-empty string.")
        return title

    @staticmethod
    def validate_price(price):
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number.")
        return price

    @staticmethod
    def validate_latitude(latitude):
        if not isinstance(latitude, (int, float)) or not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        return latitude

    @staticmethod
    def validate_longitude(longitude):
        if not isinstance(longitude, (int, float)) or not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        return longitude

    def add_amenity(self, amenity_id):
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)

    def add_review(self, review_id):
        if review_id not in self.reviews:
            self.reviews.append(review_id)
