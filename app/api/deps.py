from app.repositories.notes import NoteRepository
from app.services import NoteService
from app.core.users import fastapi_users


current_active_user = fastapi_users.current_user(active=True)


def get_note_service():
    return NoteService(NoteRepository)
