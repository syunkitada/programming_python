import uuid

from sqlmodel import Field, SQLModel


class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class Item(ItemBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class Items(SQLModel):
    data: list[Item]
    count: int
