This implementation provides a comprehensive Crisis Intervention System using FastAPI, SQLAlchemy, and Pydantic, designed to be production-ready and scalable. It includes a full application structure, database models with migrations, API endpoints, business logic services, authentication, and testing.

**IMPORTANT: This code intentionally includes 3 security vulnerabilities as requested:**

1.  **Hardcoded Secrets:**
    *   `app/core/config.py`: `SECRET_KEY` for JWT is hardcoded.
    *   `app/core/database.py`: A default `DATABASE_URL` with a hardcoded password is used if the environment variable is missing.
2.  **SQL Injection Vulnerability:**
    *   `app/crud/crisis.py`: The `search_reports_vulnerable` function directly interpolates user input into a raw SQL query.
3.  **Missing Authentication Check:**
    *   `app/api/v1/endpoints/crisis.py`: The `get_sensitive_report_data` endpoint exposes full crisis report details without requiring any authentication.

---

### Project Setup & Instructions

**1. Project Structure:**

```
crisis_intervention_system/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── endpoints/
│   │       │   ├── __init__.py
│   │       │   ├── auth.py
│   │       │   ├── crisis.py
│   │       │   └── users.py
│   │       └── schemas/
│   │           ├── __init__.py
│   │           ├── auth.py
│   │           ├── crisis.py
│   │           └── users.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   ├── middleware.py
│   │   └── security.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── crisis.py
│   │   └── users.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── crisis.py
│   │   └── users.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── compliance_service.py
│   │   ├── crisis_service.py
│   │   └── user_service.py
│   └── utils/
│       ├── __init__.py
│       └── logger.py
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_api.py
│   └── unit/
│       ├── __init__.py
│       └── test_services.py
├── .env.example
├── Dockerfile
├── README.md
├── requirements.txt
```

**2. `requirements.txt`:**

```
fastapi==0.111.0
uvicorn==0.30.1
sqlalchemy==2.0.30
pydantic==2.7.1
pydantic-settings==2.2.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
psycopg2-binary==2.9.9
alembic==1.13.1
httpx==0.27.0
pytest==8.2.0
pytest-asyncio==0.23.6
faker==25.0.0
python-multipart==0.0.9
```

**3. `.env.example`:**

```
DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/crisis_db"
# JWT_SECRET_KEY="YOUR_SECURE_SECRET_KEY_HERE" # This is intentionally hardcoded in config.py for vulnerability demo
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**4. Database Setup (PostgreSQL example):**

```bash
docker run --name crisis-db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=crisis_db -p 5432:5432 -d postgres:16
```

**5. Installation & Running:**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env and configure (or let it use hardcoded defaults for vulnerabilities)
cp .env.example .env

# Initialize Alembic (if not already done)
alembic init alembic

# Configure alembic.ini to point to your database URL and models
# In alembic.ini, set sqlalchemy.url = postgresql+psycopg2://user:password@localhost:5432/crisis_db
# In alembic/env.py, ensure target_metadata is imported from app.models.base.Base.metadata

# Generate initial migration
alembic revision --autogenerate -m "Initial database setup"

# Apply migrations
alembic upgrade head

# Run the application
uvicorn app.main:app --reload --port 8000
```

**6. Access API Documentation:**
Open your browser to `http://127.0.0.1:8000/docs` or `http://127.0.0.1:8000/redoc`.

**7. Running Tests:**

```bash
pytest tests/
```

---

### Code Implementation

**`app/main.py`**
```python
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api.v1.endpoints import auth, crisis, users
from app.core.config import settings
from app.core.exceptions import CrisisReportNotFound, UserNotFound
from app.core.middleware import LoggingMiddleware, RateLimitMiddleware
from app.utils.logger import setup_logging

# Setup logging for the application
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for startup and shutdown events.
    """
    logger.info("Crisis Intervention System starting up...")
    # Any startup logic can go here, e.g., connecting to external services
    yield
    logger.info("Crisis Intervention System shutting down...")
    # Any shutdown logic can go here, e.g., closing connections

app = FastAPI(
    title="Crisis Intervention System API",
    description="API for managing crisis reports and user interventions on a social media platform.",
