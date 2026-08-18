"""Facade Service Implementation for HBnB."""

from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository  # Use SQLAlchemy database repository
from app.persistence.review_repository import ReviewRepository  # Use SQLAlchemy database repository
from app.persistence.amenity_repository import AmenityRepository


class HBnBFacade:
    def __init__(self):
        """
        Initialize the facade with database-backed repositories.
        Using SQLAlchemy repositories ensures proper foreign key (FK) populating
        and persistent database operations instead of volatile in-memory storage.
        """
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()      # DB storage for places (avoids None owner_id)
        self.review_repo = ReviewRepository()     # DB storage for reviews (avoids None user_id)
        self.amenity_repo = AmenityRepository()

    # ==================== USER OPERATIONS ====================
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    # ==================== AMENITY OPERATIONS ====================
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity

    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)

    # ==================== PLACE OPERATIONS ====================
    def create_place(self, place_data):
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=owner.id
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None
        place.update(place_data)
        return place

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    # ==================== REVIEW OPERATIONS ====================
    def create_review(self, review_data):
        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])

        if not user or not place:
            raise ValueError("User or Place not found")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=user.id,
            place_id=place.id
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [
            r for r in self.review_repo.get_all()
            if r.place_id == place_id
        ]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
