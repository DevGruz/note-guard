from fastapi import Depends, APIRouter, Query, status

from app.api.deps import current_active_user, get_note_service
from app.schemas import NoteCreateSchema, NoteReadSchema, NoteUpdateSchema
from app.models import UserModel
from app.services import NoteService, FixErrorsOption

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: NoteCreateSchema,
    user: UserModel = Depends(current_active_user),
    note_service: NoteService = Depends(get_note_service),
    fix_errors: FixErrorsOption = Query(
        default=FixErrorsOption.NO_FIX, description="Choose error handling strategy"
    ),
) -> NoteReadSchema:
    note = await note_service.add_note(
        note_data=note_data, user_id=user.id, fix_errors=fix_errors
    )
    return note


@router.get("", status_code=status.HTTP_200_OK)
async def get_user_notes(
    user: UserModel = Depends(current_active_user),
    note_service: NoteService = Depends(get_note_service),
) -> list[NoteReadSchema]:
    notes = await note_service.get_user_notes_by_user_id(user_id=user.id)
    return notes


@router.get("/{note_id}", status_code=status.HTTP_200_OK)
async def get_user_note_by_note_id(
    note_id: int,
    user: UserModel = Depends(current_active_user),
    note_service: NoteService = Depends(get_note_service),
) -> NoteReadSchema:
    note = await note_service.get_note_by_id(note_id=note_id, user_id=user.id)
    return note


@router.patch("/{note_id}", status_code=status.HTTP_200_OK)
async def update_note(
    note_id: int,
    note_data: NoteUpdateSchema,
    user: UserModel = Depends(current_active_user),
    note_service: NoteService = Depends(get_note_service),
    fix_errors: FixErrorsOption = Query(
        default=FixErrorsOption.NO_FIX, description="Choose error handling strategy"
    ),
) -> NoteReadSchema:
    note = await note_service.update_note_by_id(
        note_id=note_id, note_data=note_data, user_id=user.id, fix_errors=fix_errors
    )
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_note_by_note_id(
    note_id: int,
    user: UserModel = Depends(current_active_user),
    note_service: NoteService = Depends(get_note_service),
):
    await note_service.delete_note_by_id(note_id=note_id, user_id=user.id)
