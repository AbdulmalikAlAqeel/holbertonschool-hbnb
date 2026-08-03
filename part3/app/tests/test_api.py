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

    def test_review_full_lifecycle(self):
        """
        Test the complete CRUD lifecycle for Review endpoints, including:
        1. Setup User and Place
        2. Create Review (POST)
        3. Get Review by ID (GET)
        4. Partial Update (PUT) & verification of updated object return
        5. Get Place Reviews (GET /places/<id>/reviews)
        6. Delete Review (DELETE)
        7. Verify Deletion (404 Not Found)
        """
        # 1. Setup prerequisite User and Place
        u_res = self.client.post('/api/v1/users/', data=json.dumps({
            "first_name": "Rev", "last_name": "User", "email": "reviewer@example.com", "password": "pass"
        }), content_type='application/json')
        u_id = u_res.get_json()['id']

        p_res = self.client.post('/api/v1/places/', data=json.dumps({
            "title": "Flat", "price": 80.0, "latitude": 24.0, "longitude": 46.0, "owner_id": u_id
        }), content_type='application/json')
        p_id = p_res.get_json()['id']

        # 2. POST: Create Review
        r_payload = {"text": "Awesome!", "rating": 5, "place_id": p_id, "user_id": u_id}
        r_res = self.client.post('/api/v1/reviews/', data=json.dumps(r_payload), content_type='application/json')
        self.assertEqual(r_res.status_code, 201)
        r_id = r_res.get_json()['id']

        # 3. GET: Fetch Review by ID
        get_res = self.client.get(f'/api/v1/reviews/{r_id}')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.get_json()['text'], "Awesome!")

        # 4. PUT: Partial Update (updating only 'text' field)
        update_payload = {"text": "Updated: Absolute perfection!"}
        put_res = self.client.put(
            f'/api/v1/reviews/{r_id}',
            data=json.dumps(update_payload),
            content_type='application/json'
        )
        self.assertEqual(put_res.status_code, 200)
        res_data = put_res.get_json()
        self.assertEqual(res_data['text'], "Updated: Absolute perfection!")
        self.assertEqual(res_data['rating'], 5)  # Rating preserved (Partial Update)
        self.assertIn('id', res_data)

        # 5. GET: Fetch Reviews for specific Place
        place_revs_res = self.client.get(f'/api/v1/places/{p_id}/reviews')
        self.assertEqual(place_revs_res.status_code, 200)
        self.assertTrue(len(place_revs_res.get_json()) > 0)

        # 6. DELETE: Delete Review
        del_res = self.client.delete(f'/api/v1/reviews/{r_id}')
        self.assertEqual(del_res.status_code, 200)

        # 7. GET: Verify deletion (should return 404)
        get_deleted = self.client.get(f'/api/v1/reviews/{r_id}')
        self.assertEqual(get_deleted.status_code, 404)

    def test_review_update_validations(self):
        """Verify strict validations during review updates"""
        # 1. Setup User and Place
        u_res = self.client.post('/api/v1/users/', data=json.dumps({
            "first_name": "Val", "last_name": "Test", "email": "val@example.com", "password": "pass"
        }), content_type='application/json')
        u_id = u_res.get_json()['id']

        p_res = self.client.post('/api/v1/places/', data=json.dumps({
            "title": "Apt", "price": 100.0, "latitude": 10.0, "longitude": 10.0, "owner_id": u_id
        }), content_type='application/json')
        p_id = p_res.get_json()['id']

        r_res = self.client.post('/api/v1/reviews/', data=json.dumps({
            "text": "Good", "rating": 4, "place_id": p_id, "user_id": u_id
        }), content_type='application/json')
        r_id = r_res.get_json()['id']

        # 2. Reject boolean rating (e.g., rating: True)
        bool_res = self.client.put(f'/api/v1/reviews/{r_id}', data=json.dumps({"rating": True}), content_type='application/json')
        self.assertEqual(bool_res.status_code, 400)

        # 3. Reject non-existent user_id
        bad_user_res = self.client.put(f'/api/v1/reviews/{r_id}', data=json.dumps({"user_id": "invalid-user-uuid"}), content_type='application/json')
        self.assertEqual(bad_user_res.status_code, 400)

        # 4. Reject non-existent place_id
        bad_place_res = self.client.put(f'/api/v1/reviews/{r_id}', data=json.dumps({"place_id": "invalid-place-uuid"}), content_type='application/json')
        self.assertEqual(bad_place_res.status_code, 400)

if __name__ == '__main__':
    unittest.main()
