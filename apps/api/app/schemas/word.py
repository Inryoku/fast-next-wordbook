from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.example import ExampleCreate, ExampleRead
from app.schemas.tag import TagRead


class WordBase(BaseModel):
    term: str
    meaning: str
    notes: str | None = None
    freq: int = 0


class WordCreate(WordBase):
    examples: list[ExampleCreate] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class WordUpdate(BaseModel):
    term: str | None = None
    meaning: str | None = None
    notes: str | None = None
    freq: int | None = None


class WordRead(WordBase):
    id: int
    created_at: datetime
    updated_at: datetime
    examples: list[ExampleRead]
    tags: list[TagRead]

    model_config = {"from_attributes": True}


class WordList(BaseModel):
    total: int
    items: list[WordRead]
