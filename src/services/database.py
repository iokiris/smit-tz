import datetime

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from src.handlers.exceptions import WebException
from src.models.cargo import Cargo, Order
from src.core.context import context as ctx


async def add_and_commit(session: AsyncSession, instance) -> None:
    session.add(instance)
    try:
        await session.commit()
        await session.refresh(instance)
    except IntegrityError:
        await session.rollback()
        raise WebException(
            code=status.HTTP_400_BAD_REQUEST,
            message="username is already in use.",
        )


async def get_cargo(date: datetime.date, cargo_type: str) -> Cargo | None:
    async with ctx.db.get_session() as session:
        cargo = await session.execute(
            select(Cargo).where((Cargo.datetime == date) & (Cargo.cargo_type == cargo_type))
        )

        result = cargo.scalars().first()
        if result:
            return result
    raise WebException(400, "Cargo not found")


async def upsert_cargo(cargo_data: Cargo):
    stmt = pg_insert(Cargo).values(
        cargo_type=cargo_data.cargo_type,
        rate=cargo_data.rate,
        datetime=cargo_data.datetime,
    )

    stmt = stmt.on_conflict_do_update(
        index_elements=['cargo_type', 'datetime'],
        set_={
            'rate': cargo_data.rate
        }
    )

    async with ctx.db.get_session() as session:
        await session.execute(stmt)
        await session.commit()


async def delete_cargo(date: datetime.date, cargo_type: str) -> None:
    async with ctx.db.get_session() as session:
        cargo = await get_cargo(date, cargo_type)
        await session.execute(
            delete(Order).where(Order.cargo_id == cargo.id)
        )

        await session.commit()

        await session.delete(cargo)
        await session.commit()
