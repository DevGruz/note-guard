from fastapi import FastAPI

from app.api.main import api_router


app = FastAPI(
    title="Note Guard",
    description="This project is a service for creating and managing notes, implemented using FastAPI. The service supports adding notes, retrieving a list of notes, and validating spelling errors using Yandex.Speller. Authentication and authorization are also implemented to ensure that users can only access their own notes.",
)

app.include_router(api_router)
