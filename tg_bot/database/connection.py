import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


class AsyncDatabaseConnection:
    def __init__(self):
        self._session = None
        self._engine = None

    @property
    def session(self) -> AsyncSession:
        return self._session

    def init(self):
        self._engine = create_async_engine(
            url=f"postgresql+asyncpg://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@{os.getenv('PG_HOST')}:"
                f"{os.getenv('PG_PORT')}/{os.getenv('PG_NAME')}"
        )
        self._session = AsyncSession(self._engine)


db = AsyncDatabaseConnection()
