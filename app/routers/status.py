from fastapi import APIRouter
from fastapi import Response
from http import HTTPStatus
from app.database.engine import check_availability
from app.models.database_status import DatabaseStatus


router = APIRouter()


@router.get("/health")
def health() -> DatabaseStatus:
    return DatabaseStatus(database=check_availability())


@router.get("/ping")
def ping():
    return Response(status_code=HTTPStatus.OK, media_type="application/json", content='{"message": "pong"}')
