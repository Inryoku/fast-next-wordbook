from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import db_session
from app.crud.tag import get_tag_by_slug, get_tag_words, get_tags
from app.schemas.tag import TagDetail, TagRead, TagWithCount, WordSummary

router = APIRouter()


@router.get("/", response_model=list[TagWithCount])
def list_tags(db: Session = Depends(db_session)) -> list[TagWithCount]:
    results = get_tags(db)
    return [TagWithCount(id=tag.id, slug=tag.slug, label=tag.label, count=count) for tag, count in results]


@router.get("/{slug}", response_model=TagDetail)
def read_tag(
    slug: str,
    db: Session = Depends(db_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
) -> TagDetail:
    tag = get_tag_by_slug(db, slug)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    total, words = get_tag_words(db, tag=tag, skip=skip, limit=limit)
    word_items = [WordSummary.model_validate(word) for word in words]
    return TagDetail(tag=TagRead.model_validate(tag), total=total, words=word_items)
