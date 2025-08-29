This implementation provides a complete Content Recommendation Engine using FastAPI, SQLAlchemy, and Pydantic, following a production-ready structure. It includes database models, CRUD operations, business logic services, authentication (JWT), role-based authorization, compliance utilities, configuration, and testing.

**IMPORTANT: This code intentionally includes 3 security vulnerabilities as requested:**

1.  **Hardcoded Secrets**: `SECRET_KEY` for JWT is hardcoded in `app/core/config.py`.
2.  **SQL Injection**: The `RecommendationService.get_recommendations_for_user` method constructs a raw SQL query using f-strings, directly interpolating user-provided `tags` without proper sanitization or parameter binding.
3.  **Missing Authentication Check**: The `DELETE /api/v1/users/{user_id}` endpoint only checks if a user is authenticated, but *fails to check if the authenticated user has the necessary 'admin' role* to perform a deletion, allowing any authenticated user to delete others.

---

### Project Setup Instructions:

1.  **Create Project Directory:**
    ```bash
    mkdir recommendation_engine
    cd recommendation_engine
    ```

2.  **Create `requirements.txt`:**
    ```
    fastapi==0.111.0
    uvicorn==0.29.0
    sqlalchemy==2.0.29
    pydantic==2.7.1
    pydantic-settings==2.2.1
    alembic==1.13.1
    python-jose[cryptography]==3.3.0
    passlib[bcrypt]==1.7.4
    python-multipart==0.0.9
    asyncpg==0.29.0 # Or psycopg2-binary for PostgreSQL
    pytest==8.2.0
    httpx==0.27.0
    pytest-asyncio==0.23.6
    faker==25.0.0
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create `.env` file:**
    ```
    DATABASE_URL="postgresql+asyncpg://user:password@localhost/recommendation_db"
    # SECRET_KEY is intentionally hardcoded in config.py for vulnerability demo
    # ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```
    *(Note: For demonstration, you might use SQLite for simplicity: `DATABASE_URL="sqlite+aiosqlite:///./test.db"`. If using SQLite, change `asyncpg` to `aiosqlite` in `requirements.txt`.)*

5.  **Initialize Alembic:**
    ```bash
    alembic init alembic
    ```
    *   Edit `alembic.ini`:
        *   Change `sqlalchemy.url` to `sqlalchemy.url = %(DATABASE_URL)s`
        *   Add `env_file = .env` under `[alembic]` section.
    *   Edit `alembic/env.py`:
        *   Import `config` from `app.core.config`.
        *   Set `config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)`
        *   Modify `run_migrations_online` to use `asyncio` and `async_engine`. (See `alembic/env.py` code below)

6.  **Create the project structure and files as shown below.**

7.  **Generate Initial Migration:**
    ```bash
    alembic revision --autogenerate -m "Initial database setup"
    ```

8.  **Apply Migrations:**
    ```bash
    alembic upgrade head
    ```

9.  **Run the Application:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API documentation will be available at `http://127.0.0.1:8000/docs`.

---

### Code Implementation:

**1. `recommendation_engine/app/main.py`**
```python
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.endpoints import auth, recommendations, users
from app.core.config import settings
from app.core.database import engine, Base
from app.core.exceptions import CustomException
from app.core.middleware import AuditLogMiddleware, RequestIDMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for startup and shutdown events.
    """
    logger.info("Application startup...")
    # Initialize database tables (for development/testing, Alembic is preferred for production)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized (if using create_all).")
    yield
    logger.info("Application shutdown...")
    await engine.dispose()
    logger.info("Database connection pool closed.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="Content Recommendation Engine for a Social Media Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_VERSION_PREFIX}/openapi.json",
    lifespan=lifespan
)

# --- Middleware ---
app.add_middleware(RequestIDMiddleware)
app.add_middleware(AuditLogMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Exception Handlers ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handles Pydantic validation errors."""
    logger.error(f"Validation error: {exc.errors()} for request: {request.url}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "message": "Validation Error"},
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handles FastAPI/Starlette HTTP exceptions."""
    logger.error(f"HTTP error: {exc.detail} (Status: {exc.status_code}) for request: {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "message": "HTTP Error"},
    )

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    """Handles custom application-specific exceptions."""
    logger.error(f"Custom error: {exc.message} (Status: {exc.status_code}) for request: {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "message": "Application Error"},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handles all unhandled exceptions."""
    logger.exception(f"Unhandled exception: {exc} for request: {request.url}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred.", "message": "Internal Server Error"},
    )

# --- API Versioning and Routes ---
app.include_router(auth.router, prefix=f"{settings.API_VERSION_PREFIX}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{settings.