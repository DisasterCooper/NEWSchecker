from sqlalchemy import (
    Column,
    String,
    Integer,
    select,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base

from tg_bot.database.connection import db

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime(), nullable=True)
    is_superuser = Column(Boolean(), nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(Boolean(), nullable=False)
    is_active = Column(Boolean(), nullable=False)
    date_joined = Column(DateTime(), nullable=False)
    phone = Column(String(20), nullable=True)
    tg_id = Column(Integer(), nullable=True)

    def __str__(self):
        return f"User: {self.id} ({self.username})"

    @classmethod
    async def get(cls, tg_id: int) -> "User":
        """
        Получение одного элемента.
        """
        query = select(cls).where(cls.tg_id == tg_id)
        async with db.session as session:
            result = await session.execute(query)
            return result.scalar_one()


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text(), nullable=False)
    link = Column(String(200), nullable=False)
    published = Column(DateTime())
    source_id = Column(ForeignKey("news_sources.id", ondelete="CASCADE"))

    @classmethod
    async def get_all(cls):
        async with db.session as session:
            result = await session.execute(select(cls))
            return result.scalars().all()
