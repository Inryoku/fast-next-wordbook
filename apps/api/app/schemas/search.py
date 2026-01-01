from pydantic import BaseModel

from app.schemas.word import WordRead


class SearchResponse(BaseModel):
    total: int
    items: list[WordRead]
