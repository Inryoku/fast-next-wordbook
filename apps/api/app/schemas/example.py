from pydantic import BaseModel


class ExampleBase(BaseModel):
    sentence: str
    source: str | None = None


class ExampleCreate(ExampleBase):
    pass


class ExampleRead(ExampleBase):
    id: int

    model_config = {"from_attributes": True}
