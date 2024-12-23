import httpx
from config import Settings
from model import JwtToken

async def payment_service_call(payment_data: dict):
    url = f"{Settings.PAYMENT_URL}/payment"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payment_data)
        return response.json()
    
async def notify_authorization_service(user_id: int, action: str):
    
    url = f"{Settings.AUTHORIZATION_URL}/api/{action}/{user_id}"
    async with httpx.AsyncClient() as client:
        response = await client.post(url)
        return response.json()

async def create_subscription(data: JwtToken):
    subs_dict = data.model_dump()

    # await SubscriptionDAO.add(**subs_data) логика взаимодействия с бд больше не нужна

    payment_status = await payment_service_call({"user_id": data.user_id})

    if payment_status.get("Success"):
        await notify_authorization_service(data.user_id, "set_sub")
    else:
        raise ValueError("Payment failed")

    return subs_dict

async def unsubscribe(data: JwtToken):
    subs_dict = data.model_dump()

    status = await notify_authorization_service(data.user_id, "unsub")

    if (status.get("Success") is not True):
        raise ValueError("Failed to notify authorization service")

    return {"Success" : True, "Message" : "Subscription is successfully canceled"}

async def checksub(data: JwtToken):
    subs_dict = data.model_dump()

    status = await notify_authorization_service(data.user_id, "checksub")  

    if (status.get("Success") is not True):
        return {"Message" : "You don't have a subscription"}
    return {"Success" : True, "Message" : "You have a subscription"}


        

