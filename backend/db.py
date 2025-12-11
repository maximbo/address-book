from typing import Annotated, AsyncGenerator, Awaitable, cast
from fastapi import Depends
from redis.asyncio import Redis

from backend.settings import settings


class DBException(Exception): ...


class ObjectNotFound(DBException): ...


class ObjectAlreadyExists(DBException): ...


_redis: Redis | None = None


class AddressBook:
    REDIS_KEY = "phone"

    def __init__(self, redis: Redis):
        self._redis = redis

    async def is_alive(self) -> bool:
        return await cast(Awaitable[bool], self._redis.ping())

    async def create(self, phone: str, address: str) -> str:
        if not await cast(
            Awaitable[bool], self._redis.hsetnx(self.REDIS_KEY, phone, address)
        ):
            raise ObjectAlreadyExists

        return address

    async def get(self, phone: str) -> str:
        address = await cast(Awaitable[str], self._redis.hget(self.REDIS_KEY, phone))
        if address is None:
            raise ObjectNotFound

        return address

    async def update(self, phone: str, address: str):
        if not await cast(Awaitable[bool], self._redis.hexists(self.REDIS_KEY, phone)):
            raise ObjectNotFound

        await cast(Awaitable[int], self._redis.hset(self.REDIS_KEY, phone, address))

        return address

    async def delete(self, phone: str):
        if not await cast(Awaitable[int], self._redis.hdel(self.REDIS_KEY, phone)):
            raise ObjectNotFound


async def connect_to_redis() -> Redis:
    global _redis

    if _redis is None:
        _redis = Redis.from_url(settings.redis_dsn)

    return _redis


async def disconnect_from_redis() -> bool:
    global _redis

    if _redis is None:
        return False

    await _redis.aclose()
    _redis = None

    return True


async def get_session() -> AsyncGenerator[AddressBook, None]:
    assert _redis is not None
    yield AddressBook(_redis)


DBSession = Annotated[AddressBook, Depends(get_session)]
