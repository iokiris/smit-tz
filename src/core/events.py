from fastapi import APIRouter
from src.controllers.kafka import kafka

router = APIRouter()


@router.on_event("shutdown")
async def shutdown():
    await kafka.stop_producer()