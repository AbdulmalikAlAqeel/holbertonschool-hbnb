# HBnB Architecture Documentation

## Task 0: High-Level Package Diagram

The high-level package diagram illustrates the three-layer architecture of the HBnB application and the communication between these layers via the facade pattern.

```mermaid
packageDiagram
    package "Presentation Layer (API)" {
        [Controllers]
    }

    package "Business Logic Layer (Core)" {
        [HBnB_Facade]
        [Entities]
    }

    package "Persistence Layer" {
        [Repository]
    }

    [Presentation Layer (API)] --> [HBnB_Facade] : Uses
    [HBnB_Facade] --> [Entities] : Manages
    [HBnB_Facade] --> [Persistence Layer] : Stores/Retrieves
