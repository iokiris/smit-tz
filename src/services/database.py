import datetime

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from src.handlers.exceptions import WebException
from src.models.cargo import Cargo
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
    cargo = await ctx.db.session.execute(
        select(Cargo).where((Cargo.datetime == date) & (Cargo.cargo_type == cargo_type))
    )

    result = cargo.scalar_one_or_none()
    if result:
        return result
    raise WebException(400, "Cargo not found")


async def upsert_cargo(cargo_data: Cargo):
    """
    Если запись с таким же cargo_type и datetime существует,
    обновляется значение rate.
    """
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

    await ctx.db.session.execute(stmt)
    await ctx.db.session.commit()