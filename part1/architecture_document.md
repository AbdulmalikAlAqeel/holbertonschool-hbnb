# HBnB Architecture Documentation

## Introduction
This document provides a comprehensive overview of the HBnB application architecture. The system is designed following a monolithic three-layer architecture utilizing the Facade Pattern to decouple thepresentation, business logic, and data persistence layers.

## Task 0: High-Level Package Diagram

The high-level package diagram illustrates the three-layer architecture of the HBnB application and the communication between these layers via the facade pattern.

```mermaid
classDiagram
    %% Presentation Layer: Handles client requests and API routes
    class Presentation_Layer_API {
        +UserController
        +PlaceController
        +ReviewController
        +AmenityController
    }

    %% Business Logic Layer: Core logic managed by the Facade pattern
    class Business_Logic_Layer_Core {
        <<Facade Pattern>>
        +HBnBAPI_Facade
        +User_Model
        +Place_Model
        +Review_Model
        +Amenity_Model
    }

    %% Persistence Layer: Database access and repository management
    class Persistence_Layer_Data {
        <<Interface>>
        +IRepository
        +InMemory_or_DB_Repository
    }

    %% Communication pathways between layers via the facade
    Presentation_Layer_API --> Business_Logic_Layer_Core : Calls via Facade
    Business_Logic_Layer_Core --> Persistence_Layer_Data : Database Operations
```

## Task 2: Sequence Diagrams for API Calls

### 1. User Registration

```mermaid
sequenceDiagram
    participant Client
    participant API as Presentation_Layer_API
    participant Facade as HBnBAPI_Facade
    participant User as User_Model
    participant Repo as IRepository
    participant DB as InMemory_or_DB_Repository

    Client->>API: POST /users
    API->>API: Validate request data
    API->>Facade: register_user(data)
    Facade->>User: create user object
    User-->>Facade: user instance
    Facade->>Repo: save(user)
    Repo->>DB: store user
    DB-->>Repo: confirmation
    Repo-->>Facade: user saved
    Facade-->>API: created user
    API-->>Client: 201 Created
```

### 2. Place Creation

```mermaid
sequenceDiagram
    participant Client
    participant API as Presentation_Layer_API
    participant Facade as HBnBAPI_Facade
    participant Place as Place_Model
    participant Repo as IRepository
    participant DB as InMemory_or_DB_Repository

    Client->>API: POST /places
    API->>API: Validate place data
    API->>Facade: create_place(data)
    Facade->>Place: create place object
    Place-->>Facade: place instance
    Facade->>Repo: save(place)
    Repo->>DB: store place
    DB-->>Repo: confirmation
    Repo-->>Facade: place saved
    Facade-->>API: created place
    API-->>Client: 201 Created
```

This diagram shows how a new place is created. The request goes from the Presentation Layer to the Facade, then the place object is created and stored in the Persistence Layer.

### 3. Review Submission

```mermaid
sequenceDiagram
    participant Client
    participant API as Presentation_Layer_API
    participant Facade as HBnBAPI_Facade
    participant Review as Review_Model
    participant Repo as IRepository
    participant DB as InMemory_or_DB_Repository

    Client->>API: POST /places/{place_id}/reviews
    API->>API: Validate review data
    API->>Facade: create_review(place_id, user_id, data)
    Facade->>Repo: get_place(place_id)
    Repo->>DB: find place
    DB-->>Repo: place data
    Repo-->>Facade: place found
    Facade->>Review: create review object
    Review-->>Facade: review instance
    Facade->>Repo: save(review)
    Repo->>DB: store review
    DB-->>Repo: confirmation
    Repo-->>Facade: review saved
    Facade-->>API: created review
    API-->>Client: 201 Created
```

This diagram shows the review submission process. The system checks that the place exists before creating and saving the review.

### 4. Fetching a List of Places

```mermaid
sequenceDiagram
    participant Client
    participant API as Presentation_Layer_API
    participant Facade as HBnBAPI_Facade
    participant Repo as IRepository
    participant DB as InMemory_or_DB_Repository

    Client->>API: GET /places?criteria
    API->>API: Validate query parameters
    API->>Facade: get_places(criteria)
    Facade->>Repo: find_places(criteria)
    Repo->>DB: retrieve matching places
    DB-->>Repo: places data
    Repo-->>Facade: list of places
    Facade-->>API: places list
    API-->>Client: 200 OK
```

This diagram shows how the application fetches a list of places. The API receives the search criteria, the Facade processes the request, and the repository retrieves matching places.

### 1. User Registration (Success & Error Handling)

sequenceDiagram
    participant Client
    participant API as Presentation_Layer_API
    participant Facade as HBnBAPI_Facade
    participant Repo as IRepository

    Client->>API: POST /users
    API->>API: Validate request data (e.g., email format)
    
    alt Data is Invalid
        API-->>Client: 400 Bad Request (Validation Error)
    else Data is Valid
        API->>Facade: register_user(data)
        Facade->>Repo: Check if email exists
        
        alt Email Already Registered
            Repo-->>Facade: User exists
            Facade-->>API: Error (Duplicate Email)
            API-->>Client: 400 Bad Request (Email already taken)
        else Email is Available
            Facade->>Repo: save(user)
            Repo-->>Facade: confirmation
            Facade-->>API: created user
            API-->>Client: 201 Created
        end
    end

## Explanatory Notes

These sequence diagrams describe the flow of four main API calls in the HBnB application: user registration, place creation, review submission, and fetching a list of places.

The Presentation Layer receives requests from the client and validates the input. The Business Logic Layer, represented by the HBnBAPI_Facade, processes the request and applies the application rules. The Persistence Layer, represented by IRepository and InMemory_or_DB_Repository, handles saving and retrieving data.

The Facade pattern helps separate the Presentation Layer from the Persistence Layer, making the application easier to organize, maintain, and extend.
