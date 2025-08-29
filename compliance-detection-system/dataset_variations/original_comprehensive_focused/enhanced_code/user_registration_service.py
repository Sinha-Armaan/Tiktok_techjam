This implementation provides a comprehensive User Registration System using FastAPI, SQLAlchemy, and Pydantic. It includes a full project structure, database models, API endpoints, business logic, authentication, testing, and compliance utilities.

**IMPORTANT: This code intentionally includes 3 security vulnerabilities as requested:**

1.  **Hardcoded Secret:** The `DATABASE_PASSWORD` is hardcoded in `app/core/config.py`.
2.  **SQL Injection:** The `get_user_by_username_unsafe` method in `app/services/user_service.py` directly interpolates user input into a raw SQL query.
3.  **Missing Input Validation (XSS):** The `UserUpdate` schema in `app/api/v1/schemas/user.py` allows `bio` and `display_name` fields to accept arbitrary strings, including HTML/script tags, without sanitization, making it vulnerable to XSS if rendered directly on a frontend.

---

## User Registration System

This project implements a user registration system for a social media platform, built with FastAPI, SQLAlchemy, and Pydantic.

### Features

*   User Registration & Login
*   JWT-based Authentication
*   User Profile Management (CRUD)
*   Role-Based Access Control (Admin/User)
*   Compliance Utilities (COPPA, GDPR)
*   Database Migrations (Alembic)
*   Comprehensive Testing (Pytest)
*   Structured Logging

### Project Structure

```
user_registration_system/
├── alembic/                          # Alembic migration scripts
│   ├── versions/
│   └── env.py
│   └── script.py.mako
├── app/
│   ├── main.py                       # FastAPI application entry point
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/            # API route definitions
│   │   │   │   ├── auth.py
│   │   │   │   └── users.py
│   │   │   └── schemas/              # Pydantic request/response models
│   │   │       ├── auth.py
│   │   │       └── user.py           # XSS vulnerability in UserUpdate
│   ├── core/
│   │   ├── config.py                 # Application settings (Hardcoded secret here!)
│   │   ├── database.py               # SQLAlchemy engine, session management
│   │   ├── security.py               # Password hashing, JWT utilities
│   │   ├── exceptions.py             # Custom application exceptions
│   │   ├── middleware.py             # Custom FastAPI middleware
│   │   └── logging.py                # Logging configuration
│   ├── models/                       # SQLAlchemy ORM models
│   │   └── user.py
│   ├── services/                     # Business logic layer
│   │   ├── auth_service.py
│   │   └── user_service.py           # SQL Injection vulnerability here!
│   ├── utils/
│   │   ├── compliance.py             # COPPA, GDPR utilities
│   │   └── email_sender.py           # Placeholder for email sending
│   └── dependencies.py               # Dependency injection functions
├── tests/
│   ├── unit/                         # Unit tests for services, utils
│   ├── integration/                  # Integration tests for API endpoints
│   └── conftest.py                   # Pytest fixtures
├── .env.example                      # Example environment variables
├── Dockerfile                        # Dockerfile for containerization
├── requirements.txt                  # Python dependencies
├── alembic.ini                       # Alembic configuration
└── README.md                         # Project README
```

### Setup and Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/user_registration_system.git
    cd user_registration_system
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the root directory based on `.env.example`.
    **Note:** The `DATABASE_PASSWORD` is hardcoded in `app/core/config.py` for demonstration of the vulnerability. In a real application, it should be loaded from environment variables or a secure secret manager.

    ```ini
    # .env
    DATABASE_URL="sqlite:///./sql_app.db"
    SECRET_KEY="your-super-secret-jwt-key" # Change this in production!
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

4.  **Run database migrations:**
    ```bash
    alembic upgrade head
    ```

5.  **Run the FastAPI application:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API documentation (Swagger UI) will be available at `http://127.0.0.1:8000/docs`.

### Running Tests

```bash
pytest
```

---

### Code Implementation

#### `requirements.txt`

```
fastapi==0.111.0
uvicorn==0.30.1
SQLAlchemy==2.0.30
alembic==1.13.1
pydantic==2.7.1
pydantic-settings==2.2.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
pytest==8.2.0
httpx==0.27.0
```

#### `alembic.ini`

```ini
[alembic]
script_location = alembic
sqlalchemy.url = sqlite:///./sql_app.db
# This is a placeholder. In a real app, it should come from config.py
# and be dynamically set in env.py.
# For this example, we'll let env.py handle it.

[post_write_hooks]
# ...
```

#### `alembic/env.py`

```python
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from app.core.config import settings
from app.models.user import Base as UserModelBase # Import your Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the SQLAlchemy URL from your application settings
config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

# add your model's MetaData object here
# for 'autogenerate' support