from fastapi import APIRouter, Response, Request

from subscription.service import create_subscription,renew_subscription
from subscription.model import Subscription, SubsPattern

router = APIRouter(prefix="/api/subscriptions", tags=["Subscriptions"])

@router.post("/create")
async def create(sub_data: SubsPattern) -> dict:
    response = await create_subscription(sub_data)
    return response

@router.patch("/autorenewal")
async def renew(user_id: int, autorenewal: bool):
    response = await renew_subscription(user_id, autorenewal)
    return response