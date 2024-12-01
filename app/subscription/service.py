from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from subscription.model import Subscription, SubscriptionDAO, SubsPattern, SubRenewPattern
from config import Settings
from database import async_session_maker

async def create_subscription(subs_data: SubsPattern):
    subs_dict = subs_data.model_dump()
    await SubscriptionDAO.add(**subs_data)
    return subs_dict

async def renew_subscription(user_id: int, autorenewal: bool):
   
    user = SubscriptionDAO.find_by_id(user_id)
    # print(user.user_id)
    return
        

