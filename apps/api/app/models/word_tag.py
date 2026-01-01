from sqlalchemy import Column, ForeignKey, Integer, Table, UniqueConstraint

from app.db.base import Base

word_tags = Table(
    "word_tags",
    Base.metadata,
    Column("word_id", Integer, ForeignKey("words.id"), nullable=False),
    Column("tag_id", Integer, ForeignKey("tags.id"), nullable=False),
    UniqueConstraint("word_id", "tag_id", name="uq_word_tags_word_id_tag_id"),
)
