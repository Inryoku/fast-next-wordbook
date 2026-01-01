# api

FastAPI app with SQLAlchemy 2.0, Alembic, and Pydantic v2.

## Setup

- Install deps: `uv sync`
- Run: `uv run uvicorn app.main:app --reload`

## Optional write protection

Set `WRITE_API_KEY` in `.env` and send `X-API-KEY` header for POST/PUT/DELETE.

## Migrations

- Generate: `uv run alembic revision --autogenerate -m "init"`
- Apply: `uv run alembic upgrade head`
