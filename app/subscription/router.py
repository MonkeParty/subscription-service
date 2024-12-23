from fastapi import APIRouter, Response, Request

from subscription.service import create_subscription, unsubscribe, checksub
from subscription.model import Subscription, JwtToken

router = APIRouter(prefix="/api/subscriptions", tags=["Subscriptions"])

@router.post("/create")
async def create(data: JwtToken):
    response = await create_subscription(data)
    return response

@router.put("/unsub")
async def delete(data: JwtToken):
    response = await unsubscribe(data)
    return response

@router.post("/check")
async def check(data:JwtToken):
    response = await checksub(data)
    return response