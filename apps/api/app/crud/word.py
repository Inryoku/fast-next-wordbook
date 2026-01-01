import re

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.example import Example
from app.models.tag import Tag
from app.models.word import Word
from app.models.word_tag import word_tags
from app.schemas.word import WordCreate, WordUpdate


def _word_query():
    return select(Word).options(selectinload(Word.examples), selectinload(Word.tags))


def _normalize_slug(raw: str) -> str:
    slug = raw.strip().lower()
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    return slug


def _unique_slugs(slugs: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for raw in slugs:
        slug = _normalize_slug(raw)
        if not slug or slug in seen:
            continue
        seen.add(slug)
        result.append(slug)
    return result

def get_words(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    sort: str = "new",
    tag: str | None = None,
) -> tuple[int, list[Word]]:
    query = _word_query()
    if tag:
        query = query.join(word_tags).join(Tag).where(Tag.slug == tag)

    if sort == "freq":
        query = query.order_by(Word.freq.desc(), Word.created_at.desc())
    else:
        query = query.order_by(Word.created_at.desc())

    count_subq = query.with_only_columns(Word.id).subquery()
    total = db.scalar(select(func.count()).select_from(count_subq)) or 0
    items = db.scalars(query.offset(skip).limit(limit)).all()
    return total, items


def get_word(db: Session, word_id: int) -> Word | None:
    return db.scalar(_word_query().where(Word.id == word_id))


def create_word(db: Session, *, payload: WordCreate) -> Word:
    word = Word(term=payload.term, meaning=payload.meaning, notes=payload.notes, freq=payload.freq)

    if payload.examples:
        word.examples = [Example(sentence=e.sentence, source=e.source) for e in payload.examples]

    if payload.tags:
        slugs = _unique_slugs(payload.tags)
        tags = db.scalars(select(Tag).where(Tag.slug.in_(slugs))).all()
        existing = {tag.slug: tag for tag in tags}
        for slug in slugs:
            tag = existing.get(slug)
            if not tag:
                label = slug.replace("-", " ").title()
                tag = Tag(slug=slug, label=label)
                db.add(tag)
            word.tags.append(tag)

    db.add(word)
    db.commit()
    db.refresh(word)
    return word


def update_word(db: Session, *, word: Word, payload: WordUpdate) -> Word:
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(word, field, value)
    db.add(word)
    db.commit()
    db.refresh(word)
    return word


def delete_word(db: Session, *, word: Word) -> None:
    db.delete(word)
    db.commit()
