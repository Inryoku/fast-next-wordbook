from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.tag import Tag
from app.models.word import Word
from app.models.word_tag import word_tags


def get_tags(db: Session) -> list[tuple[Tag, int]]:
    stmt = (
        select(Tag, func.count(word_tags.c.word_id))
        .outerjoin(word_tags, Tag.id == word_tags.c.tag_id)
        .group_by(Tag.id)
        .order_by(Tag.label.asc())
    )
    return db.execute(stmt).all()


def get_tag_by_slug(db: Session, slug: str) -> Tag | None:
    return db.scalar(select(Tag).where(Tag.slug == slug))


def get_tag_words(
    db: Session,
    *,
    tag: Tag,
    skip: int = 0,
    limit: int = 20,
) -> tuple[int, list[Word]]:
    base = (
        select(Word)
        .join(word_tags)
        .where(word_tags.c.tag_id == tag.id)
        .order_by(Word.created_at.desc())
    )
    count_subq = base.with_only_columns(Word.id).subquery()
    total = db.scalar(select(func.count()).select_from(count_subq)) or 0
    items = db.scalars(base.offset(skip).limit(limit)).all()
    return total, items
