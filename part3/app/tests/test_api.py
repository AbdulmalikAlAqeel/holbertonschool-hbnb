import unittest
import json

from flask_jwt_extended import create_access_token

from app import create_app, facade
from app.extensions import db


class HBnBAPITestCase(unittest.TestCase):
    """Test the HBnB API with JWT authentication."""

    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.drop_all()
        db.create_all()

        facade.amenity_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()

    def tearDown(self):
        self.app_context.pop()

    def create_user(
        self,
        email="user@example.com",
        password="pass123",
        first_name="John",
        last_name="Doe"
    ):
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }

        return self.client.post(
            "/api/v1/users/",
            data=json.dumps(payload),
            content_type="application/json"
        )

    def login(self, email, password="pass123"):
        response = self.client.post(
            "/api/v1/auth/login",
            data=json.dumps({
                "email": email,
                "password": password
            }),
            content_type="application/json"
        )

        return response.get_json()["access_token"]

    def auth_headers(self, token):
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def test_create_user_success(self):
        response = self.create_user()

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertIn("id", data)
        self.assertEqual(data["first_name"], "John")
        self.assertEqual(data["email"], "user@example.com")
        self.assertNotIn("password", data)

    def test_create_user_duplicate_email(self):
        self.create_user(email="duplicate@example.com")

        response = self.create_user(
            email="duplicate@example.com"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Email already registered",
            response.get_json()["error"]
        )

    def test_create_amenity_success(self):
        admin_token = create_access_token(
            identity="test-admin",
            additional_claims={"is_admin": True}
        )

        response = self.client.post(
            "/api/v1/amenities/",
            data=json.dumps({"name": "WiFi"}),
            headers=self.auth_headers(admin_token)
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertEqual(data["name"], "WiFi")
        self.assertIn("id", data)

    def test_create_place_success(self):
        self.create_user(email="owner@example.com")

        token = self.login("owner@example.com")

        response = self.client.post(
            "/api/v1/places/",
            data=json.dumps({
                "title": "Modern Apartment",
                "description": "City center",
                "price": 150.0,
                "latitude": 40.7128,
                "longitude": -74.0060,
                "amenities": []
            }),
            headers=self.auth_headers(token)
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertEqual(data["title"], "Modern Apartment")
        self.assertIn("id", data)
        self.assertIn("owner", data)

    def test_review_full_lifecycle(self):
        self.create_user(
            email="owner@example.com",
            first_name="Owner"
        )

        owner_token = self.login("owner@example.com")

        place_response = self.client.post(
            "/api/v1/places/",
            data=json.dumps({
                "title": "Flat",
                "description": "Test flat",
                "price": 80.0,
                "latitude": 24.0,
                "longitude": 46.0,
                "amenities": []
            }),
            headers=self.auth_headers(owner_token)
        )

        self.assertEqual(place_response.status_code, 201)

        place_id = place_response.get_json()["id"]

        self.create_user(
            email="reviewer@example.com",
            first_name="Reviewer"
        )

        reviewer_token = self.login("reviewer@example.com")

        review_response = self.client.post(
            "/api/v1/reviews/",
            data=json.dumps({
                "text": "Awesome!",
                "rating": 5,
                "place_id": place_id
            }),
            headers=self.auth_headers(reviewer_token)
        )

        self.assertEqual(review_response.status_code, 201)

        review_id = review_response.get_json()["id"]

        get_response = self.client.get(
            f"/api/v1/reviews/{review_id}"
        )

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(
            get_response.get_json()["text"],
            "Awesome!"
        )

        update_response = self.client.put(
            f"/api/v1/reviews/{review_id}",
            data=json.dumps({
                "text": "Updated review"
            }),
            headers=self.auth_headers(reviewer_token)
        )

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(
            update_response.get_json()["text"],
            "Updated review"
        )

        delete_response = self.client.delete(
            f"/api/v1/reviews/{review_id}",
            headers=self.auth_headers(reviewer_token)
        )

        self.assertEqual(delete_response.status_code, 200)

        deleted_response = self.client.get(
            f"/api/v1/reviews/{review_id}"
        )

        self.assertEqual(deleted_response.status_code, 404)

    def test_review_update_validations(self):
        self.create_user(email="owner@example.com")

        owner_token = self.login("owner@example.com")

        place_response = self.client.post(
            "/api/v1/places/",
            data=json.dumps({
                "title": "Apt",
                "description": "Test",
                "price": 100.0,
                "latitude": 10.0,
                "longitude": 10.0,
                "amenities": []
            }),
            headers=self.auth_headers(owner_token)
        )

        place_id = place_response.get_json()["id"]

        self.create_user(email="reviewer@example.com")

        reviewer_token = self.login("reviewer@example.com")

        review_response = self.client.post(
            "/api/v1/reviews/",
            data=json.dumps({
                "text": "Good",
                "rating": 4,
                "place_id": place_id
            }),
            headers=self.auth_headers(reviewer_token)
        )

        review_id = review_response.get_json()["id"]

        response = self.client.put(
            f"/api/v1/reviews/{review_id}",
            data=json.dumps({"rating": True}),
            headers=self.auth_headers(reviewer_token)
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
