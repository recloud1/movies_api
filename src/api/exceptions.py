from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.exceptions import NotAuthorized
from models.core import ErrorSchema


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(NotAuthorized)
    async def jwt_exception(request: Request, e: NotAuthorized):
        """
        Обработчик для ошибок авторизации
        """
        return JSONResponse(
            ErrorSchema(detail=str(e)).dict(),
            status_code=401
        )
