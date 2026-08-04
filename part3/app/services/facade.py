from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """Manage communication between the API and business models."""

    def __init__(self):
        """Initialize repositories."""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ==========================
    # USER OPERATIONS
    # ==========================

    def create_user(self, user_data):
        """Create and store a user."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email."""
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update an existing user."""
        user = self.get_user(user_id)

        if not user:
            return None

        if "email" in user_data and user_data["email"] != user.email:
            existing_user = self.get_user_by_email(
                user_data["email"]
            )

            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")

        user.update(user_data)
        return user

    # ==========================
    # AMENITY OPERATIONS
    # ==========================

    def create_amenity(self, amenity_data):
        """Create and store an amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity."""
        amenity = self.get_amenity(amenity_id)

        if not amenity:
            return None

        amenity.update(amenity_data)
        return amenity

    # ==========================
    # PLACE OPERATIONS
    # ==========================

    def create_place(self, place_data):
        """Create and store a place."""
        owner = self.get_user(place_data.get("owner_id"))

        if not owner:
            raise ValueError("Owner not found")

        amenity_ids = place_data.get("amenities", [])

        if amenity_ids is None:
            amenity_ids = []

        if not isinstance(amenity_ids, list):
            raise ValueError("Amenities must be a list")

        amenities = []

        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)

            if not amenity:
                raise ValueError(
                    "Amenity not found: {}".format(amenity_id)
                )

            amenities.append(amenity)

        place = Place(
            title=place_data.get("title"),
            description=place_data.get("description"),
            price=place_data.get("price"),
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            owner=owner
        )

        place.amenities = amenities
        self.place_repo.add(place)

        return place

    def get_place(self, place_id):
        """Retrieve a place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Validate all values before updating a place."""
        place = self.get_place(place_id)

        if not place:
            return None

        owner = place.owner

        if "owner_id" in place_data:
            owner = self.get_user(place_data["owner_id"])

            if not owner:
                raise ValueError("Owner not found")

        amenities = place.amenities

        if "amenities" in place_data:
            amenity_ids = place_data["amenities"]

            if amenity_ids is None:
                amenity_ids = []

            if not isinstance(amenity_ids, list):
                raise ValueError("Amenities must be a list")

            amenities = []

            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)

                if not amenity:
                    raise ValueError(
                        "Amenity not found: {}".format(amenity_id)
                    )

                amenities.append(amenity)

        candidate = Place(
            title=place_data.get("title", place.title),
            description=place_data.get(
                "description",
                place.description
            ),
            price=place_data.get("price", place.price),
            latitude=place_data.get(
                "latitude",
                place.latitude
            ),
            longitude=place_data.get(
                "longitude",
                place.longitude
            ),
            owner=owner
        )

        place.title = candidate.title
        place.description = candidate.description
        place.price = candidate.price
        place.latitude = candidate.latitude
        place.longitude = candidate.longitude
        place.owner = owner
        place.amenities = amenities
        place.save()

        return place

    # ==========================
    # REVIEW OPERATIONS
    # ==========================

    def create_review(self, review_data):
        """Create and store a review."""
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
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews belonging to a place."""
        place = self.get_place(place_id)

        if not place:
            return None

        reviews = self.review_repo.get_all()

        return [
            review
            for review in reviews
            if review.place_id == place_id
        ]

    def update_review(self, review_id, review_data):
        """Update an existing review."""
        review = self.get_review(review_id)

        if not review:
            return None

        if "rating" in review_data:
            rating = review_data["rating"]

            if (
                isinstance(rating, bool)
                or not isinstance(rating, int)
                or not 1 <= rating <= 5
            ):
                raise ValueError(
                    "Rating must be an integer between 1 and 5"
                )

        if "user_id" in review_data:
            user = self.get_user(review_data["user_id"])

            if not user:
                raise ValueError("User not found")

        if "place_id" in review_data:
            place = self.get_place(review_data["place_id"])

            if not place:
                raise ValueError("Place not found")

        review.update(review_data)
        return review

    def delete_review(self, review_id):
        """Delete an existing review."""
        review = self.get_review(review_id)

        if not review:
            return False

        self.review_repo.delete(review_id)
        return True
