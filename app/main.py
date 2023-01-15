from fastapi import FastAPI

from app.backend.config import config
from app.const import OPEN_API_DESCRIPTION, OPEN_API_TITLE
from app.routers import auth
from app.routers import movies
from app.version import __version__

app = FastAPI(
    title=f"{OPEN_API_TITLE} ({config.env})",
    description=OPEN_API_DESCRIPTION,
    version=__version__,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.include_router(auth.router)
app.include_router(movies.router)
