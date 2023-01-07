import inspect

from fastapi.exceptions import HTTPException
from loguru import logger


def raise_with_log(status_code: int, detail: str) -> None:
    """Wrapper function for logging and raising exceptions."""

    desc = f"<HTTPException status_code={status_code} detail={detail}>"
    logger.error(f"{desc} | runner={runner_info()}")
    raise HTTPException(status_code, detail)


def runner_info() -> str:
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f"{info.filename}:{info.function}:{info.lineno}"
