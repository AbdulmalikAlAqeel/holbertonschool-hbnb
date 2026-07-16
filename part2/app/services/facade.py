from app.persistence.repository import InMemoryRepository


from app.models import User, Amenity, Place, Review

class HBnBFacade:
    """
    Facade class that coordinates the communication between the 
    Presentation (API) layer and the Business Logic / Persistence layers.
    """
    def __init__(self):
        # Initialize in-memory repositories for each domain model
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # =========================================================================
    # USER OPERATIONS
    # =========================================================================

    def create_user(self, user_data):
        """
        Creates a new user and saves them in the repository.
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieves a single user by their unique ID.
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Retrieves a user by their email address. Useful for duplicate email validation.
        """
        all_users = self.user_repo.get_all()
        for user in all_users:
            if user.email == email:
                return user
        return None

    def get_all_users(self):
        """
        Retrieves all users stored in the system.
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """
        Updates a user's details based on their ID and new data.
        """
        return self.user_repo.update(user_id, user_data)

    # =========================================================================
    # AMENITY OPERATIONS
    # =========================================================================

    def create_amenity(self, amenity_data):
        """
        Creates a new amenity (e.g., WiFi, Pool) and saves it in the repository.
        """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Retrieves an amenity by its unique ID.
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Retrieves all amenities stored in the system.
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Updates an amenity's details.
        """
        return self.amenity_repo.update(amenity_id, amenity_data)

    # =========================================================================
    # PLACE OPERATIONS
    # =========================================================================

    def create_place(self, place_data):
        """
        Creates a new place and saves it in the repository.
        """
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """
        Retrieves a place by its unique ID.
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Retrieves all places stored in the system.
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Updates a place's details.
        """
        return self.place_repo.update(place_id, place_data)

    # =========================================================================
    # REVIEW OPERATIONS
    # =========================================================================

    def create_review(self, review_data):
        """
        Creates a new review for a place and saves it.
        """
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """
        Retrieves a review by its unique ID.
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Retrieves all reviews stored in the system.
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Retrieves all reviews submitted for a specific place.
        """
        all_reviews = self.review_repo.get_all()
        return [review for review in all_reviews if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        """
        Updates an existing review's details.
        """
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """
        Deletes a review from the system.
        """
        return self.review_repo.delete(review_id)
