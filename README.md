# next-fastapi-app

Monorepo with a Next.js (TypeScript) frontend and a FastAPI backend.

## Structure

- apps/web: Next.js app
- apps/api: FastAPI app

## Quick start

Backend (from apps/api):

- Install deps: `uv sync`
- Run API: `uv run uvicorn app.main:app --reload`

Frontend (from apps/web):

- Install deps: `npm install`
- Run web: `npm run dev`

## Local Postgres

Update `apps/api/.env` (copy from `.env.example`) to match your local Postgres.
Run Alembic migrations after creating the database.

- Generate: `uv run alembic revision --autogenerate -m "init"`
- Apply: `uv run alembic upgrade head`
