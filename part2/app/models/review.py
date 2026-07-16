from models.base_model import BaseModel

class Review(BaseModel):
    """Represents a review left by a user for a specific place."""
    
    def __init__(self, text, rating, place_id, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not text:
            raise ValueError("Review text cannot be empty.")
        self.text = text
        self.rating = self.validate_rating(rating)
        self.place_id = place_id  # Linked Place ID
        self.user_id = user_id    # Linked User ID

    @staticmethod
    def validate_rating(rating):
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        return rating
