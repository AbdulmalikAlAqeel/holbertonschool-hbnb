# HBnB API - Manual cURL Test Cases

This document provides a comprehensive suite of manual `cURL` test commands to verify and evaluate all RESTful API endpoints for the HBnB project.

---

## 📋 Table of Contents
1. [User Endpoints](#1-user-endpoints)
2. [Amenity Endpoints](#2-amenity-endpoints)
3. [Place Endpoints](#3-place-endpoints)
4. [Review Endpoints](#4-review-endpoints)
5. [Edge Cases & Error Handling](#5-edge-cases--error-handling)

---

## 1. User Endpoints

### 1.1 Create a New User (POST)
```bash
curl -X POST [http://127.0.0.1:5000/api/v1/users/](http://127.0.0.1:5000/api/v1/users/) \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "securepassword123"
  }'
