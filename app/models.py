import uuid
import datetime

from sqlalchemy import ForeignKey, text, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from fastapi_users.db import SQLAlchemyBaseUserTableUUID


class BaseModel(DeclarativeBase):
    pass


class UserModel(SQLAlchemyBaseUserTableUUID, BaseModel):
    __tablename__ = "users"

    notes: Mapped[list["NoteModel"]] = relationship("NoteModel", back_populates="user")


class NoteModel(BaseModel):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    user: Mapped["UserModel"] = relationship(back_populates="notes")
