Here's a complete, production-ready Python implementation of a Content Recommendation Engine, including the requested security vulnerabilities.

---

**IMPORTANT SECURITY WARNINGS:**

This code intentionally includes the following security vulnerabilities as requested:

1.  **Hardcoded Secrets:** The `SECRET_KEY` for JWT is hardcoded in `app/core/config.py`. In a real application, this should be loaded from environment variables, a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault), or a secure configuration system.
2.  **SQL Injection Vulnerability:** The `search_content_unsafe` endpoint and its corresponding service method in `app/services/content.py` construct a SQL query using f-strings directly with user input. This is highly vulnerable to SQL injection attacks. Always use parameterized queries or an ORM's safe query methods.
3.  **Missing Input Validation (XSS):** The `description` field in `ContentCreate` and `ContentUpdate` Pydantic models (and thus in the database model) does not perform any sanitization. If a user submits malicious HTML/JavaScript in this field and a frontend renders it directly, it will lead to a Cross-Site Scripting (XSS) attack. Input should always be sanitized (e.g., using a library like `Bleach` or `DOMPurify` on the frontend) before storage and rendering.

---

**Project Structure:**

```
.
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── v1
│   │       ├── __init__.py
│   │       ├── endpoints
│   │       │   ├── __init__.py
│   │       │   ├── auth.py
│   │       │   ├── content.py
│   │       │   ├── recommendations.py
│   │       │   └── users.py
│   │       └── models
│   │           ├── __init__.py
│   │           ├── auth.py
│   │           ├── content.py
│   │           ├── recommendation.py
│   │           └── user.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   ├── logging.py
│   │   ├── middleware.py
│   │   └── security.py
│   ├── db
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── content.py
│   │   │   ├── recommendation.py
│   │   │   └── user.py
│   │   └── session.py
│   ├── main.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── content.py
│   │   ├── recommendation.py
│   │   └── user.py
│   └── utils
│       ├── __init__.py
│       ├── audit.py
│       ├── compliance.py
│       └── feature_flags.py
├── alembic.ini
├── Dockerfile
├── requirements.txt
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── integration
    │   ├── __init__.py
    │   └── test_api.py
    └── unit
        ├── __init__.py
        ├── test_services.py
        └── test_utils.py
```

---

**1. `requirements.txt`**

```
fastapi==0.111.0
uvicorn==0.30.1
sqlalchemy==2.0.30
pydantic==2.7.1
pydantic-settings==2.2.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
alembic==1.13.1
psycopg2-binary==2.9.9
python-multipart==0.0.9
pytest==8.2.0
httpx==0.27.0
faker==25.0.0
```

---

**2. `alembic.ini`** (Standard Alembic config, adjust `sqlalchemy.url` if needed)

```ini
[alembic]
script_location = app/db/migrations
sqlalchemy.url = postgresql+psycopg2://user:password@localhost:5432/recommendation_db
revision_table_filename = alembic_version.py
version_locations = %(script_location)s/versions
output_encoding = utf-8
```

---

**3. `Dockerfile`**

```dockerfile
# Use a lightweight Python image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
# Use gunicorn for production deployment with Uvicorn workers
# CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "