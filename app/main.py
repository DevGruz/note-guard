from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.api.main import api_router


app = FastAPI(
    title="Note Guard",
    description="This project is a service for creating and managing notes, implemented using FastAPI. The service supports adding notes, retrieving a list of notes, and validating spelling errors using Yandex.Speller. Authentication and authorization are also implemented to ensure that users can only access their own notes.",
)

app.include_router(api_router)


@app.get("/favicon.ico")
async def favicon():
    external_favicon_url = "https://raw.githubusercontent.com/DevGruz/note-guard/7fde4c3e9525ef87f5aca05101d13ea82972a4f0/img/favicon.svg"
    return RedirectResponse(url=external_favicon_url)
