from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from backend.routers.address_book import router as address_book_router
from backend.routers.health import router as health_router

from backend.settings import settings
from backend import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect_to_redis()
    yield
    await db.disconnect_from_redis()


async def handle_db_object_not_found(request, ext):  # type: ignore
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


async def handle_db_object_already_exists(request, ext):  # type: ignore
    raise HTTPException(status_code=status.HTTP_409_CONFLICT)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Address Book",
        root_path=settings.api_root_path,
        open_api_url="openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    app.include_router(health_router, prefix="/v1/health")
    app.include_router(address_book_router, prefix="/v1")

    app.exception_handler(db.ObjectAlreadyExists)(handle_db_object_already_exists)
    app.exception_handler(db.ObjectNotFound)(handle_db_object_not_found)

    return app


app = create_app()
