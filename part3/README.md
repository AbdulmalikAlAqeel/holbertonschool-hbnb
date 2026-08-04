# HBnB Evolution - Part 2: Business Logic & API Endpoints

Welcome to the implementation phase of the **HBnB Evolution** project. In this part, we transition from theoretical design to writing functional, production-grade code. Using a modular **three-tier architecture**, we have built the **Presentation** (API) and **Business Logic** layers of the application using Python, Flask, and Flask-RESTx. 

To maintain clean separation of concerns and prepare the codebase for future database integration (SQLAlchemy in Part 3), we implemented the **Facade Design Pattern** alongside a robust **In-Memory Repository Pattern**.

---

## 🏗️ Architectural Overview

This project is built around a **Layered (Three-Tier) Architecture** coupled with the **Facade Pattern**:

1. **Presentation Layer (API):** Handled by Flask-RESTx. It routes incoming HTTP requests, performs payload validation, manages serialization (nested JSON responses), and outputs standardized HTTP status codes.
2. **Business Logic Layer (Domain Models):** Core entity models (`User`, `Place`, `Amenity`, `Review`) containing strict validation checks to protect data integrity at the domain level.
3. **Persistence Layer (Repositories):** An abstraction layer that currently handles temporary data management through an in-memory dictionary.

---

## Project Structure

```
part2/
├── app/
│   ├── api/
│   │   └── v1/
│   ├── models/
│   ├── persistence/
│   └── services/
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

### Directory Description

- **app/**: Main application package.
- **app/api/**: REST API endpoints.
- **app/models/**: Business models.
- **app/persistence/**: Repository layer.
- **app/services/**: Facade and business services.
- **config.py**: Application configuration classes.
- **run.py**: Application entry point.

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Move into the project:

```bash
cd holbertonschool-hbnb/part2
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the server:

```bash
python3 run.py
```

The application will be available at:

```
http://127.0.0.1:5000
```

---

## Testing

Run the application:

```bash
python3 run.py
```

You can test the endpoints using:

- curl
- Postman
- Insomnia

Example:

```bash
curl http://127.0.0.1:5000/
```

---

## Dependencies

- Flask
- Flask-RESTx

Install them with:

```bash
pip install -r requirements.txt
```
