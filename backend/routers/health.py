from fastapi import APIRouter, Response, status
from backend.db import DBSession

router = APIRouter(
    prefix="",
    tags=["health"],
)


@router.get(
    "/",
    summary="Проверка состояния сервиса",
    status_code=status.HTTP_200_OK,
    name="health:view",
)
async def check_health(
    db_session: DBSession,
):
    if await db_session.is_alive():
        return Response(status_code=status.HTTP_200_OK)

    return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
