# HBnB Architecture Documentation

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
