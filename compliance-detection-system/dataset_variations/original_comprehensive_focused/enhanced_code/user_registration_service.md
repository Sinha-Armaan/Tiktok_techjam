This implementation provides a comprehensive User Registration System using FastAPI, SQLAlchemy, Pydantic, and pytest. It adheres to many industry best practices, including type hints, PEP 8, structured logging, and dependency injection.

**IMPORTANT: As requested, this code intentionally includes 3 specific security vulnerabilities for demonstration purposes. These are clearly marked with `VULNERABILITY:` comments.**

---

## User Registration System

This system handles user registration, authentication, and basic user management for a social media platform, incorporating compliance features like COPPA and GDPR.

### Features

*   **User Registration:** Create new user accounts.
*   **User Authentication:** Login with username/password, receive JWT token.
*   **User Management:** Retrieve, update, and delete user profiles.
*   **Role-Based Access Control:** Differentiate between regular users and administrators.
*   **Compliance:**
    *   COPPA age verification during registration.
    *   GDPR data export and deletion utilities.
    *   Audit logging for sensitive actions.
*   **API Versioning:** `/api/v1/` prefix.
*   **Database:** SQLAlchemy ORM with SQLite (for simplicity, easily swappable).
*   **Testing:** Unit and integration tests with Pytest.

### Intentional Security Vulnerabilities Included

1.  **Hardcoded Secrets:** Database URL and JWT secret key are hardcoded in `config.py`.
2.  **SQL Injection:** The `search_users` service function directly embeds user input into a raw SQL query string.
3.  **Weak Encryption/Plaintext Storage:** User passwords are hashed using MD5 (a cryptographically weak algorithm) instead of a strong, modern KDF like bcrypt or Argon2.

---

### Project Structure

```
user_registration_system/
├── main.py
├── config.py
├── database.py
├── alembic.ini
├── requirements.txt
├── Dockerfile
├── README.md
├── models/
│   ├── __init__.py
│   └── user.py
├── schemas/
│   ├── __init__.py
│   ├── auth.py
│   └── user.py
├── services/
│   ├── __init__.py
│   ├── auth.py
│   └── user.py
├── api/
│   ├── __init__.py
│   └── v1/
│       ├── __init__.py
│       ├── endpoints/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   └── users.py
│       └── dependencies.py
├── core/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── middleware.py
│   └── security.py
├── compliance/
│   ├── __init__.py
│   ├── age_verification.py
│   ├── audit_log.py
│   └── gdpr.py
├── migrations/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── <timestamp>_initial_migration.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── factories/
    │   └── user_factory.py
    ├── integration/
    │   └── test_api.py
    └── unit/
        └── test_services.py
```

---

### Code Implementation

First, create the `user_registration_system` directory and the files as per the structure above.

**1. `requirements.txt`**

```txt
fastapi==0.111.0
uvicorn==0.29.0
sqlalchemy==2.0.29
pydantic==2.7.1
pydantic-settings==2.2.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
alembic==1.13.1
python-multipart==0.0.9
pytest==8.2.0
pytest-asyncio==0.23.6
httpx==0.27.0
factory-boy==2.12.0
```

**2. `config.py`**
(Contains **VULNERABILITY 1: Hardcoded Secrets**)

```python
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or defaults.
    """
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "User Registration System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # VULNERABILITY 1: Hardcoded Database URL
    # In a production environment, this should be loaded from environment variables
    # or a secure secret management system.
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    # VULNERABILITY 1: Hardcoded JWT Secret Key
    # This secret key should be a strong, randomly generated string
    # and loaded from environment variables or a secure secret management system.
    JWT_SECRET_KEY: str = "super-secret-key-that-is-not-secure-and-should-be-changed-immediately"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Compliance settings
    MIN_AGE_FOR_REGISTRATION: int = 13 # COPPA compliance

    # Admin user credentials for initial setup (should be removed or secured in prod)
    INITIAL_ADMIN_USERNAME: str = "admin"
    INITIAL_ADMIN_PASSWORD: str = "adminpass" # VULNERABILITY: Also a hardcoded secret

settings = Settings()
logger.info("Settings loaded.")
```

**3. `database.py`**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from config import settings

# Create the SQLAlchemy engine
# For SQLite, check_same_thread is needed for multi-threaded access (FastAPI uses multiple threads)
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class
# Each instance of SessionLocal will be a database session.
# The sessionmaker is configured to be an aut