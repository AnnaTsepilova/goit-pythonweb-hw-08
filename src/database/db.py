import contextlib

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from src.conf.config import config

class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autoflush=False, autocommit=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Database session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise  # Re-raise the original error
        finally:
            await session.close()

sessionmanager = DatabaseSessionManager(config.DB_URL)

async def get_db():
    async with sessionmanager.session() as session:
        yield session




# from sqlalchemy import create_engine, Integer, String, Boolean
# from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped

# DATABASE_URL = "postgresql://university:university@10.0.10.10/uni-hw6"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# class Base(DeclarativeBase):
#     pass

# class Note(Base):
#     __tablename__ = "notes"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     name: Mapped[str] = mapped_column(String(50))
#     description: Mapped[str] = mapped_column(String(250))
#     done: Mapped[bool] = mapped_column(Boolean, default=False)

# Base.metadata.create_all(bind=engine)

# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
