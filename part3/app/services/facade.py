from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """
    Facade class that manages data flow between API layer and Storage Repositories.
    """

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ==========================
    # USER OPERATIONS
    # ==========================

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None

        # Check email uniqueness if email is being updated
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = self.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")

        # Call entity update method (which triggers self.validate())
        user.update(user_data)
        self.user_repo.update(user_id, user)
        return user
    # ==========================
    # AMENITY OPERATIONS
    # ==========================

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

        # Calling update triggers entity setters and validation
        amenity.update(amenity_data)
        self.amenity_repo.update(amenity_id, amenity)
        return amenity

    # ==========================
    # PLACE OPERATIONS
    # ==========================

    def create_place(self, place_data):
        owner = self.get_user(place_data.get("owner_id"))
        if not owner:
            raise ValueError("Owner not found")

        place = Place(**place_data)
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
        if "owner_id" in place_data:
            owner = self.get_user(place_data["owner_id"])
            if not owner:
                raise ValueError("Owner not found")
        place.update(place_data)
        self.place_repo.update(place_id, place)
        return place

    # ==========================
    # REVIEW OPERATIONS
    # ==========================

    def create_review(self, review_data):
        user = self.get_user(review_data.get("user_id"))
        if not user:
            raise ValueError("User not found")

        place = self.get_place(review_data.get("place_id"))
        if not place:
            raise ValueError("Place not found")

        review = Review(
            text=review_data.get("text"),
            rating=review_data.get("rating"),
            place=place,
            user=user
        )

        self.review_repo.add(review)

        if hasattr(place, "add_review"):
            place.add_review(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return None
        reviews = self.review_repo.get_all()
        return [r for r in reviews if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        if "rating" in review_data and review_data["rating"] is not None:
            rating = review_data["rating"]
            if isinstance(rating, bool) or not isinstance(rating, int) or not (1 <= rating <= 5):
                raise ValueError("Rating must be an integer between 1 and 5")
            review.rating = rating

        if "user_id" in review_data and review_data["user_id"] is not None:
            new_user = self.get_user(review_data["user_id"])
            if not new_user:
                raise ValueError("User not found")
            review.user = new_user
            review.user_id = review_data["user_id"]

        if "place_id" in review_data and review_data["place_id"] is not None:
            new_place = self.get_place(review_data["place_id"])
            if not new_place:
                raise ValueError("Place not found")
            review.place = new_place
            review.place_id = review_data["place_id"]

        if "text" in review_data and review_data["text"] is not None:
            review.text = review_data["text"]

        if hasattr(review, "update"):
            review.update(review_data)

        self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True
