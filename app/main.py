from fastapi import FastAPI

from app.backend.config import settings
from app.const import OPEN_API_DESCRIPTION, OPEN_API_TITLE
from app.routers import auth
from app.routers import health
from app.version import __version__

app = FastAPI(
    title=f"{OPEN_API_TITLE} ({settings.env})",
    description=OPEN_API_DESCRIPTION,
    version=__version__,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.include_router(health.router)
app.include_router(auth.router)
