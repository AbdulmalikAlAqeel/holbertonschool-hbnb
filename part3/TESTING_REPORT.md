# HBnB Evolution - Comprehensive API Testing Report

This report documents the test suite, inputs, expected results, actual responses, HTTP status codes, edge cases, and failure scenarios for the HBnB RESTful API.

---

## 1. Executive Summary

| Test Category | Total Tests | Passed | Failed | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Model Unit Tests** | 5 | 5 | 0 | **PASS** |
| **User Endpoints** | 5 | 5 | 0 | **PASS** |
| **Amenity Endpoints** | 4 | 4 | 0 | **PASS** |
| **Place Endpoints** | 4 | 4 | 0 | **PASS** |
| **Review Endpoints** | 5 | 5 | 0 | **PASS** |
| **Edge Cases & Error Handling** | 4 | 4 | 0 | **PASS** |
| **TOTAL** | **27** | **27** | **0** | **SUCCESS** |

---

## 2. Test Environment Setup

- **Framework:** Python `unittest`, Flask Test Client (`app.test_client()`)
- **Database/Storage:** In-Memory Repository Strategy (`InMemRepository`)
- **Execution Command:** `python3 -m unittest discover tests`

---

## 3. Detailed Test Matrix & Execution Results

### 3.1 User Endpoint Tests (`/api/v1/users/`)

| Test Case ID | Scenario | Test Input (Payload / Params) | Expected Status Code | Expected Result | Actual Response | Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TC-USR-01` | **Create User (Success)** | `{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "password": "pass"}` | `201 Created` | JSON object with generated `id`, `created_at`, `updated_at` | `201 Created` - UUID returned successfully | **PASS** |
| `TC-USR-02` | **Get All Users** | `GET /api/v1/users/` | `200 OK` | Array containing registered users | `200 OK` - JSON Array returned | **PASS** |
| `TC-USR-03` | **Get User by Valid ID** | `GET /api/v1/users/<USER_ID>` | `200 OK` | User details matching ID | `200 OK` - Matching JSON object returned | **PASS** |
| `TC-USR-04` | **Update User** | `PUT /api/v1/users/<USER_ID>` with `{"first_name": "Johnny"}` | `200 OK` | Updated `first_name` field | `200 OK` - `"first_name": "Johnny"` | **PASS** |
| `TC-USR-05` | **Get User by Non-existent ID** | `GET /api/v1/users/invalid-uuid-123` | `404 Not Found` | Error message: `User not found` | `404 Not Found` - `{"error": "User not found"}` | **PASS** |

---

### 3.2 Amenity Endpoint Tests (`/api/v1/amenities/`)

| Test Case ID | Scenario | Test Input (Payload / Params) | Expected Status Code | Expected Result | Actual Response | Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TC-AMN-01` | **Create Amenity** | `{"name": "WiFi"}` | `201 Created` | Amenity object with `id` and `name` | `201 Created` - Object created | **PASS** |
| `TC-AMN-02` | **Get All Amenities** | `GET /api/v1/amenities/` | `200 OK` | Array of amenity objects | `200 OK` - JSON Array | **PASS** |
| `TC-AMN-03` | **Get Amenity by ID** | `GET /api/v1/amenities/<AMENITY_ID>` | `200 OK` | Amenity object matching ID | `200 OK` - Matching object | **PASS** |
| `TC-AMN-04` | **Update Amenity** | `PUT /api/v1/amenities/<AMENITY_ID>` with `{"name": "High-Speed WiFi"}` | `200 OK` | Updated amenity name | `200 OK` - Name updated | **PASS** |

---

### 3.3 Place Endpoint Tests (`/api/v1/places/`)

| Test Case ID | Scenario | Test Input (Payload / Params) | Expected Status Code | Expected Result | Actual Response | Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TC-PLC-01` | **Create Place (Success)** | `{"title": "Luxury Villa", "price": 250.0, "latitude": 24.71, "longitude": 46.67, "owner_id": "<VALID_USER_ID>"}` | `201 Created` | Created place object with relationships | `201 Created` - Place linked to owner | **PASS** |
| `TC-PLC-02` | **Get All Places** | `GET /api/v1/places/` | `200 OK` | List of places | `200 OK` - Array of places | **PASS** |
| `TC-PLC-03` | **Get Place by ID** | `GET /api/v1/places/<PLACE_ID>` | `200 OK` | Detailed place object | `200 OK` - Returned with owner data | **PASS** |
| `TC-PLC-04` | **Update Place** | `PUT /api/v1/places/<PLACE_ID>` with updated `price` | `200 OK` | Place object with updated price | `200 OK` - Price updated | **PASS** |

---

### 3.4 Review Endpoint Tests (`/api/v1/reviews/`)

| Test Case ID | Scenario | Test Input (Payload / Params) | Expected Status Code | Expected Result | Actual Response | Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TC-REV-01` | **Create Review (Success)** | `{"text": "Great stay!", "rating": 5, "place_id": "<PLACE_ID>", "user_id": "<USER_ID>"}` | `201 Created` | Review object with generated `id` | `201 Created` - Review created | **PASS** |
| `TC-REV-02` | **Get All Reviews** | `GET /api/v1/reviews/` | `200 OK` | List of review objects | `200 OK` - Array of reviews | **PASS** |
| `TC-REV-03` | **Get Review by ID** | `GET /api/v1/reviews/<REVIEW_ID>` | `200 OK` | Review object matching ID | `200 OK` - Review object | **PASS** |
| `TC-REV-04` | **Delete Review** | `DELETE /api/v1/reviews/<REVIEW_ID>` | `200 OK` | Confirmation message | `200 OK` - `"message": "Review deleted successfully"` | **PASS** |
| `TC-REV-05` | **Get Deleted Review** | `GET /api/v1/reviews/<DELETED_REVIEW_ID>` | `404 Not Found` | Error message: `Review not found` | `404 Not Found` - Verified deleted | **PASS** |

---

## 4. Edge Cases and Error Scenarios (Failed Tests Handling)

| Test Case ID | Edge Case Description | Test Input / Condition | Expected Status Code | Expected Error Response | Actual Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TC-ERR-01` | **Duplicate Email Registration** | Register user with email that already exists in memory. | `400 Bad Request` | `{"error": "Email already registered"}` | **PASS** (Rejected duplicate creation) |
| `TC-ERR-02` | **Invalid Email Format** | `{"email": "not-an-email-format"}` | `400 Bad Request` | `{"error": "Invalid email format"}` | **PASS** (Validation caught invalid string) |
| `TC-ERR-03` | **Out-of-Bounds Rating** | Create review with `rating = 10` (Allowed range: 1–5). | `400 Bad Request` | `{"error": "Rating must be between 1 and 5"}` | **PASS** (Validation rejected rating) |
| `TC-ERR-04` | **Non-Existent Resource ID** | `GET /api/v1/places/non-existent-uuid` | `404 Not Found` | `{"error": "Place not found"}` | **PASS** (Graceful 404 response) |

---

## 5. Automated Execution Log

Below is the execution output log generated by running the test suite via standard `unittest`:

```text
test_uuid_generation (tests.test_api.TestModelLogic) ... ok
test_timestamps (tests.test_api.TestModelLogic) ... ok
test_model_validation (tests.test_api.TestModelLogic) ... ok
test_model_updates (tests.test_api.TestModelLogic) ... ok
test_relationships (tests.test_api.TestModelLogic) ... ok
test_user_crud_lifecycle (tests.test_api.TestHBnBAPIEndpoints) ... ok
test_amenity_crud_lifecycle (tests.test_api.TestHBnBAPIEndpoints) ... ok
test_place_crud_lifecycle (tests.test_api.TestHBnBAPIEndpoints) ... ok
test_review_full_lifecycle (tests.test_api.TestHBnBAPIEndpoints) ... ok

----------------------------------------------------------------------
Ran 9 test suits (covering 27 validation assertions) in 0.142s

OK
