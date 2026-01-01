from collections.abc import Generator

from fastapi import Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db


def db_session() -> Generator[Session, None, None]:
    yield from get_db()


def verify_write_key(x_api_key: str | None = Header(default=None, alias="X-API-KEY")) -> None:
    if not settings.write_api_key:
        return
    if x_api_key != settings.write_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
