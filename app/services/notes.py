import uuid
from enum import Enum

from app.exceptions import NoteAccessDeniedException, SpellingErrorException
from app.schemas import NoteCreateSchema, NoteReadSchema, NoteUpdateSchema
from app.repositories import NoteRepository
from app.utils.speller import speller


class FixErrorsOption(str, Enum):
    NO_FIX = "no_fix"
    NOTIFY = "notify"
    AUTO_FIX = "auto_fix"


class NoteService:
    def __init__(self, repository: NoteRepository):
        self.repository = repository

    async def _check_spelling_note(self, title: str, content: str) -> dict[str, str]:
        corrected_texts = await speller.spelled_texts(title, content)
        errors = {}

        if corrected_texts[0] != title:
            errors["note_title"] = {
                "original": title,
                "corrected": corrected_texts[0],
            }
        if corrected_texts[1] != content:
            errors["note_content"] = {
                "original": content,
                "corrected": corrected_texts[1],
            }

        return errors

    async def add_note(
        self,
        note_data: NoteCreateSchema,
        user_id: uuid.UUID,
        fix_errors: FixErrorsOption = FixErrorsOption.NO_FIX,
    ) -> NoteReadSchema:
        if fix_errors == FixErrorsOption.NOTIFY:
            errors = await self._check_spelling_note(
                title=note_data.title, content=note_data.content
            )

            if errors:
                raise SpellingErrorException(detail=errors)

        elif fix_errors == FixErrorsOption.AUTO_FIX:
            corrected_texts = await speller.spelled_texts(
                note_data.title, note_data.content
            )
            note_data.title = corrected_texts[0] or note_data.title
            note_data.content = corrected_texts[1] or note_data.content

        note_model = await self.repository.add_one(
            **note_data.model_dump(), user_id=user_id
        )
        note_schema = NoteReadSchema.model_validate(note_model, from_attributes=True)
        return note_schema

    async def get_user_notes_by_user_id(
        self,
        user_id: uuid.UUID,
    ) -> list[NoteReadSchema]:
        note_models = await self.repository.find_all(user_id=user_id)
        note_schemas = [
            NoteReadSchema.model_validate(note_model, from_attributes=True)
            for note_model in note_models
        ]
        return note_schemas

    async def get_note_by_id(
        self,
        note_id: int,
        user_id: uuid.UUID,
    ) -> NoteReadSchema:
        note_model = await self.repository.find_one_or_none(id=note_id, user_id=user_id)
        if note_model is None:
            raise NoteAccessDeniedException()

        note_schema = NoteReadSchema.model_validate(note_model, from_attributes=True)
        return note_schema

    async def update_note_by_id(
        self,
        note_id: int,
        note_data: NoteUpdateSchema,
        user_id: uuid.UUID,
    ) -> NoteReadSchema:
        note_model = await self.repository.update_one(
            note_id=note_id, user_id=user_id, **note_data.model_dump(exclude_none=True)
        )
        if note_model is None:
            raise NoteAccessDeniedException()

        note_schema = NoteReadSchema.model_validate(note_model, from_attributes=True)
        return note_schema

    async def delete_note_by_id(
        self,
        note_id: int,
        user_id: uuid.UUID,
    ) -> None:
        note_model = await self.repository.delete_one(id=note_id, user_id=user_id)
        if note_model is None:
            raise NoteAccessDeniedException()
