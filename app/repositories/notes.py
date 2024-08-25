from sqlalchemy import delete, insert, select, update

from app.core.db import async_session_maker
from app.models import NoteModel


class NoteRepository:
    model = NoteModel

    @classmethod
    async def add_one(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            stmt = select(cls.model).filter_by(**filter_by)
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            stmt = select(cls.model).filter_by(**filter_by)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def update_one(cls, note_id: int, **data):
        async with async_session_maker() as session:
            stmt = (
                update(cls.model)
                .where(cls.model.id == note_id, cls.model.user_id == data["user_id"])
                .values(**data)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def delete_one(cls, **filter_by):
        async with async_session_maker() as session:
            stmt = delete(cls.model).filter_by(**filter_by).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one_or_none()
