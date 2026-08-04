from app.persistence.repository import InMemoryRepository
from app.models import User, Amenity, Place, Review


class HBnBFacade:
    """Facade coordinating the API, business logic and persistence layers."""

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ---------------- USER ----------------

    def create_user(self, user_data):
        email = user_data.get("email")
        if self.get_user_by_email(email):
            raise ValueError("Email already registered")

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

        new_email = user_data.get("email")
        existing = self.get_user_by_email(new_email)

        if existing and existing.id != user_id:
            raise ValueError("Email already registered")

        user.update(user_data)
        return user

    # ---------------- AMENITY ----------------

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

    # ---------------- PLACE ----------------

    def create_place(self, place_data):
        owner = self.get_user(place_data.get("owner_id"))
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title=place_data.get("title"),
            description=place_data.get("description"),
            price=place_data.get("price"),
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            owner=owner
        )

        amenity_ids = place_data.get("amenities", []) or []

        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError("Amenity not found")
            place.add_amenity(amenity)

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

        data = dict(place_data)

        if "owner_id" in data:
            owner = self.get_user(data.pop("owner_id"))
            if not owner:
                raise ValueError("Owner not found")
            place.owner = owner

        if "amenities" in data:
            amenity_ids = data.pop("amenities") or []
            amenities = []

            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError("Amenity not found")
                amenities.append(amenity)

            place.amenities = amenities

        place.update(data)
        return place

    # ---------------- REVIEW ----------------

    def create_review(self, review_data):

        """
        Create a new review using entity references for User and Place.
        """
        # 1. Fetch and validate user entity existence
        user = self.user_repo.get(review_data.get('user_id'))
        if not user:
            raise ValueError("User not found")

        # 2. Fetch and validate place entity existence
        place = self.place_repo.get(review_data.get('place_id'))

        user = self.get_user(review_data.get("user_id"))
        if not user:
            raise ValueError("User not found")

        place = self.get_place(review_data.get("place_id"))

        if not place:
            raise ValueError("Place not found")

        # 3. Instantiate Review passing actual entity instances (place, user)
        review = Review(

            text=review_data.get('text'),
            rating=review_data.get('rating'),
            place=place,
            user=user
        )          

        # 4. Save review in the repository
        self.review_repo.add(review)

        # 5. Link review instance (or review.id) to the place
        if hasattr(place, 'add_review'):
            place.add_review(review)

            text=review_data.get("text"),
            rating=review_data.get("rating"),
            place=place,
            user=user
        )

        self.review_repo.add(review)
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

        return list(place.reviews)

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        data = dict(review_data)

        if "user_id" in data:
            user = self.get_user(data.pop("user_id"))
            if not user:
                raise ValueError("User not found")
            review.user = user

        if "place_id" in data:
            new_place = self.get_place(data.pop("place_id"))
            if not new_place:
                raise ValueError("Place not found")

            old_place = review.place

            if review in old_place.reviews:
                old_place.reviews.remove(review)

            review.place = new_place
            new_place.add_review(review)

        review.update(data)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)

        if not review:
            return False

        if review in review.place.reviews:
            review.place.reviews.remove(review)

        return self.review_repo.delete(review_id)
