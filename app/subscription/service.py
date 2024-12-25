import httpx
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException, Header
from config import Settings
from model import JwtToken

def decode_jwt_token(auth_header: str) -> JwtToken:
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    
    token = auth_header[7:]

    try:
        decoded_token = jwt.decode(token, Settings.ACCESS_SECRET_KEY, algorithms=Settings.ALGORITHM)
        return decoded_token
    
    except ExpiredSignatureError:
        raise ValueError("Token has expired")
    except InvalidTokenError:
        raise ValueError("Invalid token")


async def payment_service_call(payment_data: dict):
    url = f"{Settings.PAYMENT_URL}/payment"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payment_data)
        return response.json()
    
async def notify_aсcount_service(user_id: int, action: str):
    url = f"{Settings.ACCOUNT_URL}/api/{action}/{user_id}"
    async with httpx.AsyncClient() as client:
        response = await client.post(url)
        return response.json()

async def create(auth: str = Header(...)):
    try:
        data = decode_jwt_token(auth)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    payment_status = await payment_service_call({"user_id": data.id})

    if payment_status.get("Success"):
        await notify_aсcount_service(data.id, "set_sub")
        return {"status" : "Subscription successful"}
    else:
        raise HTTPException(status_code=400, detail="Payment failed")

async def delete(auth: str = Header(...)):
    try:
        data = decode_jwt_token(auth)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        status = await notify_aсcount_service(data.id, "unsub")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to communicate with account service")
    
    if not status.get("Success"):
        raise HTTPException(status_code=400, detail="Failed to cancel subscription")

    return {"Success": True, "Message": "Subscription successfully canceled"}

async def check(auth: str = Header(...)):
    try:
        data = decode_jwt_token(auth)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if (data.has_sub == True):
        return {"Success": True, "Message" : "User has a subscription"}
    return {"Failed" : False, "Message" : "User has not a subscription"}