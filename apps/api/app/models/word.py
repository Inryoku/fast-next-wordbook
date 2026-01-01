from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.word_tag import word_tags


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    term: Mapped[str] = mapped_column(String(255), index=True)
    meaning: Mapped[str] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    freq: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    examples: Mapped[list["Example"]] = relationship(
        back_populates="word", cascade="all, delete-orphan"
    )
    tags: Mapped[list["Tag"]] = relationship(secondary=word_tags, back_populates="words")
