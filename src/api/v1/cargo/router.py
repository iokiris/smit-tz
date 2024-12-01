import datetime

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from src.core import settings
from src.core.context import context
from src.models.cargo import Cargo, Order
from src.schemas.cost import CargoCost
from src.services import database

router = APIRouter(tags=["cargo manage"])


@router.post("/update-costs")
async def update_costs(tariffs: CargoCost = Depends()):
    updated = 0
    for date, cargos in tariffs.data.items():
        for cargo in cargos:
            await database.upsert_cargo(Cargo(
                cargo_type=cargo.cargo_type,
                rate=cargo.rate,
                datetime=date
            ))
            updated += 1
    return JSONResponse(f"{updated} cargos updated")


@router.delete("/update-costs")
async def delete_costs(date: datetime.date, cargo_type: str):
    await database.delete_cargo(date, cargo_type)
    return JSONResponse({
        "message": f"{cargo_type} cargo from {date} successfully deleted"
    })


@router.get("/calculate-cost")
async def calculate_cost(date: datetime.date, cargo_type: str):
    cargo = await database.get_cargo(date, cargo_type)
    if cargo:
        order_price = settings.declared_cost * cargo.rate
        cargo_order = Order(cargo_id=cargo.id, price=order_price)
        await database.add_and_commit(
            context.db.session,
            cargo_order,
        )
        return JSONResponse({
            "price": order_price
        })

