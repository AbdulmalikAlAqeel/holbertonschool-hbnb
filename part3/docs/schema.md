# HBnB - Database Entity-Relationship (ER) Diagram

Below is the Entity-Relationship diagram representing the database schema for the HBnB project, including `User`, `Place`, `Review`, `Amenity`, and the join table `Place_Amenity`.

![HBnB ER Diagram](part3/docs/mermaid-diagram.png)

```mermaid
erDiagram
    USER ||--o{ PLACE : "owns"
    USER ||--o{ REVIEW : "writes"
    PLACE ||--o{ REVIEW : "has"
    PLACE ||--|{ PLACE_AMENITY : "contains"
    AMENITY ||--|{ PLACE_AMENITY : "included_in"

    USER {
        string id PK
        string email
        string password
        string first_name
        string last_name
        datetime created_at
        datetime updated_at
    }

    PLACE {
        string id PK
        string user_id FK
        string name
        string description
        float number_rooms
        float number_bathrooms
        float max_guest
        float price_by_night
        float latitude
        float longitude
        datetime created_at
        datetime updated_at
    }

    REVIEW {
        string id PK
        string place_id FK
        string user_id FK
        string text
        integer rating
        datetime created_at
        datetime updated_at
    }

    AMENITY {
        string id PK
        string name
        datetime created_at
        datetime updated_at
    }

    PLACE_AMENITY {
        string place_id FK
        string amenity_id FK
    }
```
