from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from contextlib import asynccontextmanager
import os
from src.models.base import Base
load_dotenv(".env.auth")


DATABASE_URL = os.getenv("DATABASE_URL")


class Database:
    def __init__(
            self,
            url: str,
            echo: bool = False,
            pool_size: int = 5,
            max_overflow: int = 10,
            pool_timeout: int = 10
    ) -> None:
        self._engine = create_async_engine(
            url=url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout
        )
        self._async_session = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            expire_on_commit=False,
            autoflush=False,
        )

    @property
    def session(self) -> AsyncSession:
        return self._async_session()

    @property
    def engine(self):
        return self._engine

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        async with self._async_session() as session:
            yield session

    async def create_all(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def ping(self) -> bool:
        """
        Пинг базы данных
        :return: True | False
        """
        print("Trying to ping db...")
        try:
            async with self.engine.connect() as conn:
                result = await conn.execute(select(1))
                if result.scalar() == 1:
                    print("Database connection successful (Ping OK).")
                    return True

        except SQLAlchemyError as e:
            print(f"Error connecting to the database: {e}")
            return False

        except Exception:
            return False

        finally:
            await self._engine.dispose()

    async def close(self) -> None:
        await self._engine.dispose()


def create_database(url: str) -> Database:
    return Database(url=url)