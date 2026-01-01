from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Example(Base):
    __tablename__ = "examples"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id"), index=True)
    sentence: Mapped[str] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)

    word: Mapped["Word"] = relationship(back_populates="examples")
