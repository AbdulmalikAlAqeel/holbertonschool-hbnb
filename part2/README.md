# HBnB Evolution - Part 2: Business Logic & API Endpoints

Welcome to the implementation phase of the **HBnB Evolution** project. In this part, we transition from theoretical design to writing functional, production-grade code. Using a modular **three-tier architecture**, we have built the **Presentation** (API) and **Business Logic** layers of the application using Python, Flask, and Flask-RESTx. 

To maintain clean separation of concerns and prepare the codebase for future database integration (SQLAlchemy in Part 3), we implemented the **Facade Design Pattern** alongside a robust **In-Memory Repository Pattern**.

---

## 🏗️ Architectural Overview

This project is built around a **Layered (Three-Tier) Architecture** coupled with the **Facade Pattern**:

1. **Presentation Layer (API):** Handled by Flask-RESTx. It routes incoming HTTP requests, performs payload validation, manages serialization (nested JSON responses), and outputs standardized HTTP status codes.
2. **Business Logic Layer (Domain Models):** Core entity models (`User`, `Place`, `Amenity`, `Review`) containing strict validation checks to protect data integrity at the domain level.
3. **Persistence Layer (Repositories):** An abstraction layer that currently handles temporary data management through an in-memory dictionary.
