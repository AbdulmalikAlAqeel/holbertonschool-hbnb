import time
import unittest
import uuid

from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.user import User


class TestModels(unittest.TestCase):
    """Test HBnB business models."""

    def setUp(self):
        """Create valid objects for tests."""
        self.user = User(
            email="owner@example.com",
            first_name="Khaled",
            last_name="Yousef"
        )

        self.place = Place(
            title="Test Place",
            description="A test place",
            price=100.0,
            latitude=24.7136,
            longitude=46.6753,
            owner=self.user
        )

        self.amenity = Amenity("Wi-Fi")

    def test_uuid_is_valid_and_unique(self):
        """Test UUID generation."""
        another_user = User(
            email="other@example.com",
            first_name="Other",
            last_name="User"
        )

        uuid.UUID(self.user.id)
        uuid.UUID(another_user.id)

        self.assertNotEqual(
            self.user.id,
            another_user.id
        )

    def test_timestamps_and_save(self):
        """Test timestamp management."""
        old_updated_at = self.user.updated_at

        time.sleep(0.01)
        self.user.save()

        self.assertIsNotNone(self.user.created_at)
        self.assertGreater(
            self.user.updated_at,
            old_updated_at
        )

    def test_update(self):
        """Test valid updates."""
        old_updated_at = self.user.updated_at

        time.sleep(0.01)
        self.user.update({
            "first_name": "Ahmed"
        })

        self.assertEqual(
            self.user.first_name,
            "Ahmed"
        )
        self.assertGreater(
            self.user.updated_at,
            old_updated_at
        )

    def test_invalid_user_names(self):
        """Test invalid user names."""
        with self.assertRaises(ValueError):
            User(
                email="test@example.com",
                first_name="A" * 51,
                last_name="User"
            )

        with self.assertRaises(ValueError):
            User(
                email="test@example.com",
                first_name="Test",
                last_name=""
            )

    def test_invalid_email(self):
        """Test invalid email."""
        with self.assertRaises(ValueError):
            User(
                email="invalid-email",
                first_name="Test",
                last_name="User"
            )

    def test_invalid_place_values(self):
        """Test invalid place data."""
        with self.assertRaises(ValueError):
            Place(
                title="Test",
                description="Test",
                price=0,
                latitude=0,
                longitude=0,
                owner=self.user
            )

        with self.assertRaises(ValueError):
            Place(
                title="Test",
                description="Test",
                price=10,
                latitude=91,
                longitude=0,
                owner=self.user
            )

        with self.assertRaises(ValueError):
            Place(
                title="Test",
                description="Test",
                price=10,
                latitude=0,
                longitude=181,
                owner=self.user
            )

        with self.assertRaises(ValueError):
            Place(
                title="Test",
                description="Test",
                price=10,
                latitude=0,
                longitude=0,
                owner="invalid-owner"
            )

    def test_invalid_amenity_name(self):
        """Test invalid amenity names."""
        with self.assertRaises(ValueError):
            Amenity("A" * 51)

    def test_review_validation(self):
        """Test review validation."""
        with self.assertRaises(ValueError):
            Review(
                "",
                5,
                self.place,
                self.user
            )

        with self.assertRaises(ValueError):
            Review(
                "Good",
                True,
                self.place,
                self.user
            )

        with self.assertRaises(ValueError):
            Review(
                "Good",
                6,
                self.place,
                self.user
            )

        with self.assertRaises(ValueError):
            Review(
                "Good",
                5,
                "invalid-place",
                self.user
            )

        with self.assertRaises(ValueError):
            Review(
                "Good",
                5,
                self.place,
                "invalid-user"
            )

    def test_relationships(self):
        """Test entity relationships."""
        review = Review(
            text="Excellent",
            rating=5,
            place=self.place,
            user=self.user
        )

        self.place.add_amenity(self.amenity)
        self.place.add_review(review)

        self.assertIs(
            self.place.owner,
            self.user
        )
        self.assertIn(
            self.amenity,
            self.place.amenities
        )
        self.assertIn(
            review,
            self.place.reviews
        )
        self.assertIs(
            review.place,
            self.place
        )
        self.assertIs(
            review.user,
            self.user
        )
        self.assertEqual(
            self.place.owner_id,
            self.user.id
        )
        self.assertEqual(
            review.place_id,
            self.place.id
        )
        self.assertEqual(
            review.user_id,
            self.user.id
        )


if __name__ == "__main__":
    unittest.main()
