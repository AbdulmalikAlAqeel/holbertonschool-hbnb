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
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        for user in self.user_repo.get_all():
            if user.email == email:
                return user
        return None

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)

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
        return self.amenity_repo.update(amenity_id, amenity_data)

    # ---------------- PLACE (Task 4) ----------------
    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        amenities_ids = place_data.get('amenities', []) or []

        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description', ''),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner_id=owner_id
        )

        for amenity_id in amenities_ids:
            if not self.amenity_repo.get(amenity_id):
                raise ValueError("Amenity {} not found".format(amenity_id))
            place.add_amenity(amenity_id)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        if 'owner_id' in place_data and not self.user_repo.get(place_data['owner_id']):
            raise ValueError("Owner not found")

        if 'amenities' in place_data:
            amenities_ids = place_data.pop('amenities') or []
            for amenity_id in amenities_ids:
                if not self.amenity_repo.get(amenity_id):
                    raise ValueError("Amenity {} not found".format(amenity_id))
            place.amenities = amenities_ids

        if 'title' in place_data:
            Place.validate_title(place_data['title'])
        if 'price' in place_data:
            Place.validate_price(place_data['price'])
        if 'latitude' in place_data:
            Place.validate_latitude(place_data['latitude'])
        if 'longitude' in place_data:
            Place.validate_longitude(place_data['longitude'])

        place.update(place_data)
        return place

    # ---------------- REVIEW (Task 5) ----------------
    def create_review(self, review_data):
        user = self.user_repo.get(review_data.get('user_id'))
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(review_data.get('place_id'))
        if not place:
            raise ValueError("Place not found")

        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            place_id=review_data.get('place_id'),
            user_id=review_data.get('user_id')
        )
        self.review_repo.add(review)
        place.add_review(review.id)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return [r for r in self.review_repo.get_all() if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        if 'rating' in review_data:
            Review.validate_rating(review_data['rating'])
        if 'text' in review_data and not review_data['text']:
            raise ValueError("Review text cannot be empty.")
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        place = self.place_repo.get(review.place_id)
        if place and review_id in place.reviews:
            place.reviews.remove(review_id)
        return self.review_repo.delete(review_id)
