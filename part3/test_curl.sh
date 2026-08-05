#!/bin/bash
# HBnB API Quick Testing Script

BASE_URL="http://127.0.0.1:5000/api/v1"

echo "=== 1. Testing Login ==="
# Retrieve access token for regular user
USER_TOKEN=$(curl -s -X POST $BASE_URL/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "userpass123"}' | jq -r '.access_token')

# Retrieve access token for administrator account
ADMIN_TOKEN=$(curl -s -X POST $BASE_URL/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@example.com", "password": "adminpass123"}' | jq -r '.access_token')

echo "User Token: $USER_TOKEN"
echo "Admin Token: $ADMIN_TOKEN"

echo -e "\n=== 2. Testing Public Amenities ==="
# Retrieve list of amenities (Public Endpoint)
curl -s -X GET $BASE_URL/amenities/

echo -e "\n\n=== 3. Testing Admin Amenity Creation ==="
# Create a new amenity using Admin privileges (Admin-Only Endpoint)
curl -s -X POST $BASE_URL/amenities/ \
     -H "Authorization: Bearer $ADMIN_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name": "Swimming Pool"}'

echo -e "\n\nDone Testing!"
