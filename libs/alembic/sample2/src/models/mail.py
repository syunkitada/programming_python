from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Mail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    second_name: str
    email: str
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
