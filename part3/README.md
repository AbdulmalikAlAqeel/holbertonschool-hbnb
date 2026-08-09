# HBnB - Part 3: Database Storage & Persistence

Welcome to **Part 3** of the HBnB project. In this section, we transition our application's persistence layer from a file-based storage mechanism (JSON) to a robust relational database management system using **MySQL** and **SQLAlchemy ORM**.

---

## 📌 Project Overview

The objective of Part 3 is to integrate a relational database to handle data persistence securely and efficiently. By leveraging Object-Relational Mapping (ORM) via SQLAlchemy, the application bridges the gap between Python classes and database tables, allowing smooth data manipulation, object querying, and relationship management.

---

## 🛠️ Tech Stack & Key Technologies

* **Language:** Python 3.x
* **Framework:** Flask / Flask-RESTx
* **Database:** MySQL
* **ORM:** SQLAlchemy
* **Diagramming:** Mermaid.js
* **Version Control:** Git & GitHub

---

## 📁 Directory Structure

```text
part3/
├── api/                   # API routes, namespaces, and endpoints
├── models/                # SQLAlchemy database models (User, Place, Review, Amenity)
├── persistence/           # Database setup and repository interfaces
├── docs/                  # Project documentation and visual schemas
│   ├── schema.md          # ER Diagram documentation in Mermaid.js
│   └── mermaid-diagram.png # Exported ER Diagram image
├── config.py              # Environment configuration settings
├── app.py                 # Application entry point
└── README.md              # Documentation for Part 3



📐 Database Entity-Relationship (ER) DiagramThe database schema is structured around five core tables: users, places, reviews, amenities, and the association table place_amenity.

Entity Relationships Summary:


User $\leftrightarrow$ Place: One-to-Many (User can own multiple Places).

User $\leftrightarrow$ Review: One-to-Many (User can write multiple Reviews).

Place $\leftrightarrow$ Review: One-to-Many (Place can have multiple Reviews).

Place $\leftrightarrow$ Amenity: Many-to-Many (Linked via Place_Amenity bridge table).

💡 For detailed Mermaid.js code, visit docs/schema.md.

🚀 Setup & Installation Instructions

1.PrerequisitesEnsure

you have MySQL installed and running on your system, along with Python 3.8+.

2. Database Configuration

Create the MySQL database and setup user privileges:

SQL

CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;

3. Environment Variables

Set the required environment variables for database connections:

export HBNB_ENV="db"
export HBNB_MYSQL_USER="hbnb_dev"
export HBNB_MYSQL_PWD="hbnb_dev_pwd"
export HBNB_MYSQL_HOST="localhost"
export HBNB_MYSQL_DB="hbnb_dev_db"

4. Install Dependencies & Run

Install the necessary Python packages and start the application server:

pip install -r requirements.txt
python3 app.py

🧪 Testing

To run the automated test suite for the database storage layer:

pytest tests/

👤 Author

Binaqeel Abdulmalik - Aloraini Khalid - Aljohani Afnan GitHub Repository: https://github.com/AbdulmalikAlAqeel/holbertonschool-hbnb.git
