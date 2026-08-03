from app.models.base import BaseModel

class Review(BaseModel):
    """Represents a review left by a user for a specific place."""
    
    def __init__(self, text, rating, place, user):
        super().__init__()
        # Strict validation
        if not text:
            raise ValueError("Review text is required")
        if isinstance(rating, bool) or not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        if not place:
            raise ValueError("Place object is required")
        if not user:
            raise ValueError("User object is required")

        self.text = text
        self.rating = rating
        
        # Entity References (actual Python objects)
        self.place = place
        self.user = user

        # Foregin Key IDs mapped from the object references
        self.place_id = place.id if hasattr(place, 'id') else place
        self.user_id = user.id if hasattr(user, 'id') else user

    @staticmethod
    def validate_rating(rating):
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        return rating
