from fastapi import HTTPException, status


class NoteException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class NoteAccessDeniedException(NoteException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "You do not have permission to access this note."


class NoteNotFoundError(NoteException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "The requested note does not exist."


class SpellingErrorException(NoteException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = {"msg": "There are spelling errors in the text"}

    def __init__(self, detail: dict | None = None):
        if detail is None:
            detail = {}
        self.detail.update(detail)
        super().__init__()
