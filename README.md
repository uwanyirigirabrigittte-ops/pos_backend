# Bijoux's Store POS API

A FastAPI-based Point of Sale backend for inventory, sales, and employee management.

## Features

- **RESTful API** for managing products, categories, suppliers, customers, sales, and employees
- **JWT authentication** with role-based access control (admin / cashier)
- **Password hashing** via `pwdlib`
- **SQLite fallback** for local development; PostgreSQL in production

## Project Structure

```
app/
  core/          # Security utilities (hashing, JWT tokens)
  models/        # SQLAlchemy models
  repositories/  # Data access layer
  schemas/       # Pydantic schemas
  services/      # Business logic
  routers/       # API endpoints
  main.py        # FastAPI app entry point
  database.py    # Database configuration
  dependencies.py # FastAPI auth dependencies
tests/         # Pytest test suite
```

## Setup

### Local Development

```bash
# Clone the repository
git clone https://github.com/uwanyirigirabrigittte-ops/pos_backend.git
cd pos_backend

# Create and activate a virtual environment
python -m venv env
source env/bin/activate

# Install dependencies
pip install -r app/requirements.txt

# Run the server
fastapi dev app
```

The server starts at `http://127.0.0.1:8000`.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./local.db` |
| `JWT_SECRET_KEY` | Secret for JWT signing | `change-me-to-a-secret-key-32-chars` |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration (minutes) | `60` |

## Authentication

- `POST /users/login` — Login with username/password, returns a JWT `access_token`
- `POST /users/` — Create a new user (admin only, requires bearer token)
- Role `cashier` cannot create accounts; role `admin` can

Use the token in subsequent requests:

```
Authorization: Bearer <access_token>
```

## Running Tests

```bash
# Install test dependencies
pip install -r app/requirements.txt
pip install pytest httpx

# Run the full test suite
pytest tests/ -v
```

Tests use **SQLite in-memory** (isolated from the PostgreSQL dev database). All fixtures create fresh tables per test and clean up afterwards.
