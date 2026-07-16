import unittest
import json
from app import create_app, facade

class HBnBAPITestCase(unittest.TestCase):
    """
    Test suite for testing the HBnB API endpoints (Users, Amenities, Places, Reviews).
    """
    def setUp(self):
        """
        Executed before each test. Sets up the Flask test client 
        and resets the in-memory repositories for complete isolation.
        """
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Deep reset of in-memory storages to ensure clean state for every single test
        facade.user_repo._storage.clear()
        facade.amenity_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()

    def tearDown(self):
        """
        Executed after each test. Pops the application context.
        """
        self.app_context.pop()

    # =========================================================================
    # USER ENDPOINT TESTS
    # =========================================================================

    def test_create_user_success(self):
        """Test successful registration of a new user."""
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
        response = self.client.post('/api/v1/users/', 
                                    data=json.dumps(payload), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], "John")
        self.assertEqual(data['email'], "john.doe@example.com")

    def test_create_user_duplicate_email(self):
        """Test that registering a duplicate email returns an HTTP 400 error."""
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "duplicate@example.com"
        }
        # First registration
        self.client.post('/api/v1/users/', data=json.dumps(payload), content_type='application/json')
        # Second registration with same email
        response = self.client.post('/api/v1/users/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email already registered", response.get_json()['message'])

    # =========================================================================
    # AMENITY ENDPOINT TESTS
    # =========================================================================

    def test_create_amenity_success(self):
        """Test successful creation of a new amenity."""
        payload = {"name": "WiFi"}
        response = self.client.post('/api/v1/amenities/', 
                                    data=json.dumps(payload), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], "WiFi")

    # =========================================================================
    # PLACE ENDPOINT TESTS
    # =========================================================================

    def test_create_place_success(self):
        """Test creating a place linked to a valid registered owner."""
        # 1. First, create the owner
        user_payload = {"first_name": "Host", "last_name": "One", "email": "host@example.com"}
        user_res = self.client.post('/api/v1/users/', data=json.dumps(user_payload), content_type='application/json')
        owner_id = user_res.get_json()['id']

        # 2. Create the place
        place_payload = {
            "title": "Modern Apartment",
            "description": "City center",
            "price": 150.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": owner_id,
            "amenity_ids": []
        }
        response = self.client.post('/api/v1/places/', 
                                    data=json.dumps(place_payload), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['title'], "Modern Apartment")
        self.assertEqual(data['owner']['id'], owner_id)

    # =========================================================================
    # REVIEW ENDPOINT TESTS (INCLUDING DELETE)
    # =========================================================================

    def test_review_lifecycle(self):
        """Test creating, reading, updating, and deleting a review."""
        # 1. Setup User
        user_res = self.client.post('/api/v1/users/', 
                                    data=json.dumps({"first_name": "Reviewer", "last_name": "User", "email": "rev@example.com"}), 
                                    content_type='application/json')
        user_id = user_res.get_json()['id']

        # 2. Setup Place
        place_res = self.client.post('/api/v1/places/', 
                                    data=json.dumps({"title": "Cabin", "price": 99.0, "latitude": 45.0, "longitude": -45.0, "owner_id": user_id}), 
                                    content_type='application/json')
        place_id = place_res.get_json()['id']

        # 3. Create Review (POST)
        review_payload = {
            "text": "Great stay!",
            "rating": 5,
            "place_id": place_id,
            "user_id": user_id
        }
        review_res = self.client.post('/api/v1/reviews/', data=json.dumps(review_payload), content_type='application/json')
        self.assertEqual(review_res.status_code, 201)
        review_id = review_res.get_json()['id']

        # 4. Check that Place details now dynamically render this review
        place_details = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(len(place_details.get_json()['reviews']), 1)

        # 5. Delete Review (DELETE)
        del_res = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(del_res.status_code, 200)

        # 6. Check that review was deleted from everywhere
        get_deleted = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_deleted.status_code, 404)

if __name__ == '__main__':
    unittest.main()
