# Ecommerce Microservice API

A learning-oriented ecommerce microservice built with FastAPI, SQLite, SQLAlchemy, Alembic, Redis, and Docker.

The project was developed incrementally through milestone-based stages, evolving from a simple MVP into a more realistic ecommerce backend while keeping the codebase clean, documented, testable, portable, and easy to extend.

---

## Features

### Products API
- Create products.
- Retrieve products with pagination (`page` defaults to 1; `page_size` defaults to 20 and is capped at 100).
- Return page items and pagination metadata; products are ordered by ID ascending.
- Retrieve a single product.
- Pydantic validation.
- Seeded demo inventory.
- Redis-backed caching for product list and product detail retrieval.

The product list supports pagination:

```http
GET /products?page=1&page_size=20
```

`page` starts at 1 and defaults to 1. `page_size` defaults to 20 and accepts values from 1 to 100. The response contains `items`, `page`, `page_size`, `total`, and `total_pages`; items are ordered by product ID ascending.

### Shopping Cart API
- Add products to cart.
- Merge duplicate cart items.
- View cart contents.
- Remove individual items.
- Clear entire cart.
- Validate stock availability.

### Orders API
- Checkout cart items.
- Validate stock during checkout.
- Create order records and order items.
- Persist order history.
- Decrement inventory.
- Clear cart after purchase.
- Retrieve all orders.
- Retrieve individual orders.
- Nested serialization using eager loading.
- Cache invalidation after inventory-changing operations.

### Order Lifecycle API
- Order status support.
- Status transitions.
- Order cancellation rules.
- State-machine style workflow validation.
- Swagger-visible status fields.

### Payments API
- Mock payment creation for orders.
- Payment amount tracking.
- Payment provider tracking.
- Payment status tracking.
- Payment-to-user association.
- Payment-to-order association.
- Order-aware mock payment workflow.
- Database-backed payment persistence.
- Alembic-managed payments schema evolution.

### Background Tasks
- Invoice generation after checkout.
- Order-created notification generation.
- Order-status-updated notification generation.
- Order-cancelled notification generation.
- FastAPI `BackgroundTasks` integration for deferred side effects.
- Local file-based background task outputs for invoices and notifications.
- Timezone-aware UTC timestamps for generated artifacts.

### Authentication API
- User registration.
- User login.
- JWT access tokens.
- Password hashing with bcrypt.
- Protected user route.
- Swagger OAuth2 password flow.
- Redis-backed login rate limiting.

### Multi-user Ecommerce API
- User-owned cart items.
- User-owned orders.
- User-scoped cart access.
- User-scoped order access.
- Per-user checkout flow.
- Ownership protection for order retrieval and updates.
- Protected cart and order endpoints.

### Production Readiness Improvements
- Centralized runtime configuration via `app/config.py`.
- Environment-variable-driven settings using `pydantic-settings`.
- Safe committed `.env.example` for local setup and deployment reference.
- FastAPI lifespan-based startup initialization for seeded demo inventory.
- Standardized HTTP and validation error responses.
- Cleaner configuration flow across auth, database, and Redis integrations.
- Improved Docker Compose startup readiness with Redis healthcheck dependency.
- Removal of duplicated settings loading across modules.

### Database Migration Support
- Alembic integration for schema migrations.
- Initial baseline migration.
- SQLite-compatible migration configuration.
- Database revision tracking with `alembic_version`.
- Version-controlled schema evolution for future changes.
- Payments table migration added and verified.

### Testing
- Pytest-based automated test suite.
- Shared fixtures with `conftest.py`.
- Isolated SQLite test database.
- FastAPI dependency overrides for test isolation.
- In-memory `FakeRedis` test client for cache and rate-limit isolation.
- Auth, products, cart, orders, and payments endpoint coverage.
- Background task side-effect coverage for invoices and notifications.
- CI-ready test baseline.

### Docker Support
- Dockerized FastAPI application.
- `Dockerfile` for container image builds.
- `docker-compose.yml` for local container orchestration.
- Redis service included in Docker Compose.
- Redis healthcheck and health-gated API dependency in Compose.
- `.dockerignore` for cleaner build context.
- Environment-variable-based configuration.
- Container healthcheck using `/health`.

### Infrastructure
- SQLite database.
- SQLAlchemy ORM.
- Alembic migrations.
- Redis caching.
- Redis-backed rate limiting.
- Pydantic schemas.
- `pydantic-settings` configuration management.
- Dependency injection.
- Seed initialization.
- Swagger/OpenAPI documentation.
- Docker.
- Docker Compose.
- Environment variables.
- Container healthchecks.
- Background task file outputs.

Swagger UI available at:

```text
/docs
```

---

## Configuration

Copy the example environment file and adjust values as needed:

```bash
cp .env.example .env
```

Current configurable settings include:
- `DATABASE_URL`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `APP_HOST`
- `APP_PORT`
- `REDIS_URL`
- `PRODUCT_CACHE_TTL`
- `RATE_LIMIT_TIMES`
- `RATE_LIMIT_SECONDS`

Notes:
- `.env.example` is committed as a safe template.
- `.env` remains local and should not be committed.
- Application settings are centralized in `app/config.py`.

---

## Running Tests

Run the full automated test suite with:

```bash
pytest -q
```

Current baseline:
- 14 tests passing.
- Coverage includes authentication, products, cart, orders, payments, and background-task side effects.
- Tests run against an isolated SQLite test database using shared fixtures and FastAPI dependency overrides.
- Redis-dependent features are tested with an in-memory `FakeRedis` client.
- Background task flows are verified through generated invoice and notification artifacts.
- The test suite runs against the FastAPI app directly and does not require starting the server manually.
- Current known warning: `passlib` emits a Python `crypt` deprecation warning on Python 3.12+, but the suite still passes successfully.

---

## Running Migrations

Create or update the local database schema with:

```bash
alembic upgrade head
```

Check the currently applied migration with:

```bash
alembic current
```

Current migration baseline:
- Initial schema migration: `6f5e3d5e8133`
- Payments migration: `14051421d3f0`
- Verified local database head: `14051421d3f0 (head)`
- Verified `payments` table present in SQLite after upgrade
- Stage 15 introduced no new schema changes

---

## Running with Docker

Build and start the containerized application with:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Useful endpoints:
- `/docs`
- `/health`

Current Docker baseline:
- Containerized FastAPI app.
- Redis included as a Compose service.
- Environment variables loaded from `.env`.
- Redis service healthcheck enabled in Compose.
- API service waits on healthy Redis before startup.
- Container healthcheck enabled for API validation.

---

## Status

### Completed Milestones

✅ Stage 1 — FastAPI Base Setup  
Completed: 2026-06-18

Implemented:
- FastAPI application.
- SQLite database.
- SQLAlchemy setup.
- Database session dependency.
- Health endpoint.
- Seed mechanism.
- Swagger documentation.

---

✅ Stage 2 — Products API  
Completed: 2026-06-19

Implemented:
- Product model.
- CRUD operations.
- Validation schemas.
- Seeded demo products.

---

✅ Stage 3 — Cart System  
Completed: 2026-06-20

Implemented:
- Add to cart.
- Merge duplicate items.
- View cart.
- Remove item.
- Clear cart.
- Stock validation.

---

✅ Stage 4 — Orders System and Router Refactor  
Completed: 2026-06-26

Implemented:
- Checkout endpoint.
- Order creation.
- Order items.
- Inventory decrement.
- Empty cart after checkout.
- Nested serialization.
- Eager loading.
- Router modularization.
- Products router.
- Cart router.
- Orders router.
- Reduced `main.py` complexity.
- Preserved existing API behavior.
- Preserved OpenAPI compatibility.

---

✅ Stage 5 — Order Lifecycle Management  
Completed: 2026-06-29

Implemented:
- Order status support.
- `PENDING`, `PAID`, `PROCESSING`, `SHIPPED`, `DELIVERED`, `CANCELLED` statuses.
- `PATCH /orders/{id}/status`.
- `POST /orders/{id}/cancel`.
- Transition validation.
- Cancellation rules.
- Swagger verification of order status workflow.

---

✅ Stage 6 — Authentication  
Completed: 2026-07-03

Implemented:
- User model.
- User registration.
- User login.
- Password hashing.
- JWT token generation.
- OAuth2 password flow in Swagger.
- Protected route: `GET /auth/me`.
- Token-based user lookup.

---

✅ Stage 7 — Multi-user Ecommerce  
Completed: 2026-07-07

Implemented:
- User ownership for cart items.
- User ownership for orders.
- Authenticated cart endpoints.
- Authenticated order endpoints.
- User-scoped cart queries.
- User-scoped order queries.
- Per-user checkout behavior.
- Ownership checks for order access and modification.
- Swagger-documented 404 responses for inaccessible orders.

---

✅ Stage 8 — Architecture Refactor  
Completed: 2026-07-08

Implemented:
- Service-layer extraction for cart logic.
- Service-layer extraction for order logic.
- `app/services/cart_service.py`.
- `app/services/order_service.py`.
- Thinner API route handlers.
- Cleaner separation between routing and business logic.
- Preserved Swagger behavior.
- Preserved multi-user ownership isolation.
- Improved maintainability and extensibility.

---

✅ Stage 9 — Alembic  
Completed: 2026-07-09

Implemented:
- Alembic installation and initialization.
- Migration environment setup.
- SQLAlchemy metadata integration.
- Initial baseline migration.
- Database version tracking with `alembic_version`.
- SQLite-compatible migration configuration.

---

✅ Stage 10 — Testing  
Completed: 2026-07-10

Implemented:
- Pytest installation and test setup.
- `httpx` test dependency support.
- Shared fixtures in `tests/conftest.py`.
- Dedicated SQLite test database for isolated test runs.
- FastAPI dependency overrides for database isolation.
- Refactored auth database access to use dependency injection.
- Endpoint tests for authentication flows.
- Endpoint tests for product retrieval.
- Endpoint tests for cart operations.
- Endpoint tests for order creation and retrieval.
- Verified passing test baseline with 9 total tests.

---

✅ Stage 11 — Docker  
Completed: 2026-07-11

Implemented:
- Added `Dockerfile` for containerizing the FastAPI app.
- Added `docker-compose.yml` for local container orchestration.
- Added `.dockerignore` to reduce Docker build context noise.
- Updated `.gitignore` for local environment and cache hygiene.
- Moved database configuration to environment variables.
- Moved auth configuration to environment variables.
- Added `.env`-driven runtime configuration.
- Added Docker healthcheck using the `/health` endpoint.
- Verified successful container build and healthy runtime state.

---

✅ Stage 12 — Redis Caching & Rate Limiting  
Completed: 2026-07-13

Implemented:
- Added Redis integration for application caching.
- Added Redis-backed caching for product list and product detail endpoints.
- Added cache invalidation after inventory-changing operations.
- Added Redis-backed login rate limiting.
- Added Redis service to `docker-compose.yml`.
- Added `app/redis_client.py` for centralized Redis client configuration.
- Added cache utility support for invalidation workflows.
- Updated tests to use an in-memory `FakeRedis` client.
- Verified passing test baseline with Redis-aware test isolation.

---

✅ Stage 13 — Background Tasks  
Completed: 2026-07-16

Implemented:
- Added FastAPI `BackgroundTasks` to order workflows.
- Added invoice generation after successful checkout.
- Added order-created notification generation.
- Added order-status-updated notification generation.
- Added order-cancelled notification generation.
- Added `app/services/invoice_service.py`.
- Added `app/services/notification_service.py`.
- Stored generated outputs in `storage/invoices/` and `storage/notifications/`.
- Updated order routes to trigger deferred side effects after the response is sent.
- Added tests covering invoice creation and notification generation.
- Updated generated timestamps to use timezone-aware UTC datetimes.
- Added `storage/` to `.gitignore` to exclude generated artifacts from version control.
- Verified passing test baseline with 11 total tests.

---

✅ Stage 14 — Mock Payments  
Completed: 2026-07-16

Implemented:
- Added mock payment support to the ecommerce backend.
- Added `payments` table with Alembic-managed schema migration.
- Added payment fields for order association, user association, amount, provider, status, and creation timestamp.
- Added payment status enum with `PENDING`, `PAID`, and `FAILED`.
- Linked payments to existing users and orders through foreign keys.
- Verified corrected Alembic migration chain from initial migration to payments migration.
- Verified successful `alembic upgrade head` execution on SQLite.
- Verified local database head at `14051421d3f0`.
- Verified `payments` table exists in the migrated SQLite database.
- Added or updated automated tests for payment-related functionality.
- Verified passing test baseline with 14 total tests.

---

✅ Stage 15 — Production Readiness  
Completed: 2026-07-18

Implemented:
- Centralized runtime configuration in `app/config.py`.
- Added `pydantic-settings` for environment-driven application settings.
- Added committed `.env.example` for safe local and deployment setup.
- Removed duplicated per-module settings loading.
- Moved seeded demo product initialization into FastAPI lifespan startup.
- Added standardized HTTP exception responses.
- Added standardized validation error responses.
- Improved Docker Compose startup reliability with Redis healthcheck dependency.
- Removed the stray invalid dependency entry from `requirements.txt`.
- Verified passing test baseline with 14 total tests.
- Verified Alembic remained at `14051421d3f0 (head)`.
- Verified no new schema changes were introduced.

---

## Current Architecture

### Application

```text
app/
├── api/                    # API route handlers
│   ├── __init__.py
│   ├── auth.py             # Authentication endpoints
│   ├── products.py         # Product endpoints with caching
│   ├── cart.py             # User-scoped cart endpoints
│   ├── orders.py           # User-scoped order endpoints with background tasks
│   └── payments.py         # Mock payment endpoints
├── services/               # Business logic and supporting workflows
│   ├── __init__.py
│   ├── cart_service.py     # Cart business logic
│   ├── invoice_service.py  # Invoice file generation
│   ├── notification_service.py # Order notification file generation
│   ├── order_service.py    # Order business logic
│   └── payment_service.py  # Mock payment workflow logic
├── auth_utils.py           # Password hashing, JWT, auth dependency
├── cache_utils.py          # Cache invalidation helpers
├── config.py               # Centralized application settings
├── database.py             # Database connection/session setup
├── main.py                 # FastAPI application entry point and lifespan/error handlers
├── models.py               # SQLAlchemy models, including Payment
├── redis_client.py         # Redis client setup
├── rate_limiter.py         # Login rate limiting dependency
├── schemas.py              # Pydantic schemas
└── seed.py                 # Seed initial product data

alembic/
├── env.py                                  # Alembic environment configuration
├── script.py.mako                          # Migration template
└── versions/                               # Migration revision files
    ├── 6f5e3d5e8133_initial_migration.py
    └── 14051421d3f0_add_payments_table.py

tests/
├── __init__.py
├── conftest.py             # Shared pytest fixtures, test DB setup, FakeRedis
├── test_auth.py            # Authentication endpoint tests
├── test_products.py        # Product endpoint tests
├── test_cart.py            # Cart endpoint tests
├── test_orders.py          # Order endpoint tests and background-task verification
├── test_payments.py        # Payment endpoint and workflow tests

storage/                    # Runtime-generated artifacts, ignored by Git
├── invoices/               # Generated invoice files
└── notifications/          # Generated notification files
```

### Root Files

```text
requirements.txt        # Python dependencies
Dockerfile              # Docker image definition
docker-compose.yml      # Local container orchestration
.dockerignore           # Docker build context exclusions
.gitignore              # Git exclusions, including generated storage artifacts
.env                    # Local environment variables (not committed)
.env.example            # Safe example environment configuration
alembic.ini             # Alembic configuration
ecommerce.db            # SQLite database (dev only)
README.md               # Project documentation
CODE_OF_CONDUCT.md      # Community standards
CONTRIBUTING.md         # Contribution guide
LICENSE                 # Project license
```

The router modularization was introduced after Stage 4, the service layer was added in Stage 8, Alembic migration support was added in Stage 9, automated testing support was added in Stage 10, Docker support was added in Stage 11, Redis-backed caching and rate limiting were added in Stage 12, background task support for invoices and notifications was added in Stage 13, mock payment support was added in Stage 14, and production-readiness hardening was completed in Stage 15 to improve configuration hygiene, startup behavior, deployment clarity, error consistency, regression safety, and maintainability.

---

## Development Roadmap

| Stage | Description | Status |
| --- | --- | --- |
| 1 | FastAPI Setup | ✅ |
| 2 | Products API | ✅ |
| 3 | Cart System | ✅ |
| 4 | Orders System and Router Refactor | ✅ |
| 5 | Order Lifecycle Management | ✅ |
| 6 | Authentication | ✅ |
| 7 | Multi-user Ecommerce | ✅ |
| 8 | Architecture Refactor | ✅ |
| 9 | Alembic | ✅ |
| 10 | Testing | ✅ |
| 11 | Docker | ✅ |
| 12 | Caching | ✅ |
| 13 | Background Tasks | ✅ |
| 14 | Mock Payments | ✅ |
| 15 | Production Readiness | ✅ |

---

## Next Work

With implementation stages complete and the core documentation finalized, future repository work may include:
- Release notes and changelog improvements.
- Deployment examples and operational documentation.
- Further documentation improvements as the project evolves.

---

## Last Updated

2026-07-18 – completed production readiness hardening (Stage 15)

2026-07-17 – completed mock payments support and verified Alembic payments migration (Stage 14)

2026-07-16 – completed background tasks for invoices and order notifications (Stage 13)

2026-07-13 – completed Redis caching and login rate limiting (Stage 12)

2026-07-11 – completed Docker containerization (Stage 11)

2026-07-10 – completed testing baseline with pytest (Stage 10)

2026-07-09 – completed Alembic integration (Stage 9)

2026-07-08 – completed architecture refactor (Stage 8)

2026-07-07 – completed multi-user ecommerce (Stage 7)

2026-07-03 – completed Authentication (Stage 6)

2026-06-30 – completed order lifecycle management (Stage 5)

2026-06-26 – completed orders system and router refactor (Stage 4)

2026-06-20 – completed Cart System (Stage 3)

2026-06-19 – completed Products API (Stage 2)

2026-06-18 – completed FastAPI Base Setup (Stage 1)

---

## Tech Stack

- Python.
- FastAPI.
- SQLite.
- SQLAlchemy.
- Alembic.
- Redis.
- Pydantic.
- Pydantic-Settings.
- Dependency injection.
- JWT.
- OAuth2 password flow.
- Password hashing.
- Swagger/OpenAPI.
- Service-layer architecture.
- Pytest.
- HTTPX.
- Automated API testing.
- Docker.
- Docker Compose.
- Environment variables.
- Container healthchecks.
- Caching.
- Rate limiting.
- Background tasks.
- File-based side-effect generation.
- Mock payment workflow modeling.
- Production-readiness configuration hardening.
