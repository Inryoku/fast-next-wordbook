from pydantic import BaseModel


class TagBase(BaseModel):
    slug: str
    label: str


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int

    model_config = {"from_attributes": True}


class TagWithCount(TagRead):
    count: int


class WordSummary(BaseModel):
    id: int
    term: str
    meaning: str

    model_config = {"from_attributes": True}


class TagDetail(BaseModel):
    tag: TagRead
    total: int
    words: list[WordSummary]
