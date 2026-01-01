from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.api.deps import db_session
from app.models.tag import Tag
from app.models.word import Word
from app.models.word_tag import word_tags
from app.schemas.search import SearchResponse

router = APIRouter()


@router.get("/", response_model=SearchResponse)
def search_words(
    *,
    db: Session = Depends(db_session),
    q: str = Query(..., min_length=1),
    tag: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort: str = Query("new", pattern="^(new|freq)$"),
) -> SearchResponse:
    query = select(Word).options(selectinload(Word.examples), selectinload(Word.tags))
    query = query.where(Word.term.ilike(f"%{q}%"))

    if tag:
        query = query.join(word_tags).join(Tag).where(Tag.slug == tag)

    if sort == "freq":
        query = query.order_by(Word.freq.desc(), Word.created_at.desc())
    else:
        query = query.order_by(Word.created_at.desc())

    count_subq = query.with_only_columns(Word.id).subquery()
    total = db.scalar(select(func.count()).select_from(count_subq)) or 0
    items = db.scalars(query.offset(skip).limit(limit)).all()
    return SearchResponse(total=total, items=items)
