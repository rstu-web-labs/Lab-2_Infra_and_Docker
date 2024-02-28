from http import HTTPStatus

from fastapi import APIRouter, Response

from app.core.constants.mime import MimeTypes
from app.core.db import check_db_connection


router = APIRouter(include_in_schema=False)


@router.get("/liveness")
async def liveness() -> Response:
    return Response(
        status_code=HTTPStatus.OK,
        content="ok",
        media_type=MimeTypes.TEXT,
    )


@router.get("/readiness")
async def readiness() -> Response:
    if await check_db_connection():
        return Response(
            status_code=HTTPStatus.OK,
            content="ok",
            media_type=MimeTypes.TEXT,
        )
