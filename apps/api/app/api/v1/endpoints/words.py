from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import db_session, verify_write_key
from app.crud.word import create_word, delete_word, get_word, get_words, update_word
from app.schemas.word import WordCreate, WordList, WordRead, WordUpdate

router = APIRouter()


@router.get("/", response_model=WordList)
def list_words(
    *,
    db: Session = Depends(db_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort: str = Query("new", pattern="^(new|freq)$"),
    tag: str | None = None,
) -> WordList:
    total, items = get_words(db, skip=skip, limit=limit, sort=sort, tag=tag)
    return WordList(total=total, items=items)


@router.get("/{word_id}", response_model=WordRead)
def read_word(word_id: int, db: Session = Depends(db_session)) -> WordRead:
    word = get_word(db, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    return word


@router.post("/", response_model=WordRead, status_code=status.HTTP_201_CREATED)
def create_word_endpoint(
    payload: WordCreate,
    db: Session = Depends(db_session),
    _: None = Depends(verify_write_key),
) -> WordRead:
    return create_word(db, payload=payload)


@router.put("/{word_id}", response_model=WordRead)
def update_word_endpoint(
    word_id: int,
    payload: WordUpdate,
    db: Session = Depends(db_session),
    _: None = Depends(verify_write_key),
) -> WordRead:
    word = get_word(db, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    return update_word(db, word=word, payload=payload)


@router.delete("/{word_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_word_endpoint(
    word_id: int,
    db: Session = Depends(db_session),
    _: None = Depends(verify_write_key),
) -> None:
    word = get_word(db, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    delete_word(db, word=word)
