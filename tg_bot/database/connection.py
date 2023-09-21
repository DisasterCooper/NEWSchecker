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
            url="postgresql+asyncpg:///checker:password@localhost/checker_db",  # TODO заменить на os.environ.get('DATABASE_URL')
        )
        self._session = AsyncSession(self._engine)


db = AsyncDatabaseConnection()
