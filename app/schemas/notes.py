import uuid
import datetime

from pydantic import BaseModel


class NoteCreateSchema(BaseModel):
    title: str
    content: str


class NoteReadSchema(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    user_id: uuid.UUID


class NoteUpdateSchema(BaseModel):
    title: str | None = None
    content: str | None = None
