from fastapi import APIRouter, Response, Request

from subscription.service import create, delete, check
from subscription.model import Subscription, JwtToken

router = APIRouter(prefix="/api/sub", tags=["Subs"])

@router.post("/set_sub")
async def set_sub(data: JwtToken):
    response = await create(data)
    return response

@router.put("/unsub")
async def unsub(data: JwtToken):
    response = await delete(data)
    return response

@router.post("/check_sub")
async def check_sub(data:JwtToken):
    response = await check(data)
    return response