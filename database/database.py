from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, BigInteger, Boolean, DateTime, Text, func
import datetime
from config import Config

engine = create_async_engine(Config.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), nullable=True)
    first_name: Mapped[str] = mapped_column(String(250), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

class MatchAlert(Base):
    __tablename__ = "match_alerts"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    match_id: Mapped[int] = mapped_column(BigInteger, index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

class PublishedContent(Base):
    __tablename__ = "published_content"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content_type: Mapped[str] = mapped_column(String(50))  # news, match_event, daily_update
    external_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    published_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def is_content_published(external_id: str) -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            sqlalchemy.select(PublishedContent).where(PublishedContent.external_id == str(external_id))
        )
        return result.scalar_one_or_none() is not None

async def mark_content_published(content_type: str, external_id: str):
    async with AsyncSessionLocal() as session:
        item = PublishedContent(content_type=content_type, external_id=str(external_id))
        session.add(item)
        try:
            await session.commit()
        except Exception:
            await session.rollback()

import sqlalchemy
