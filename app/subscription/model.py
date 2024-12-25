from sqlalchemy import text, Date, select
from sqlalchemy.orm import Mapped, mapped_column

from pydantic import BaseModel, Field

from database import Base, str_unique_not_null, int_pk, str_nullable, str_not_null, date_not_null, async_session_maker
from dao.base import BaseDAO

from datetime import date


class Subscription(Base):
    id: Mapped[int_pk]  # Уникальный идентификатор подписки
    user_id: Mapped[int] = mapped_column(nullable=False)  # Ссылка на пользователя, владеющего подпиской

    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"), nullable=False)  # Активность подписки
    autorenewal: Mapped[bool] = mapped_column(default=False, server_default=text("false"), nullable=False)  # Включено ли автопродление

    start_date: Mapped[Date] = mapped_column(date_not_null)  # Дата начала подписки
    end_date: Mapped[Date] = mapped_column(date_not_null)  # Дата окончания подписки

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, user_id={self.user_id}, is_active={self.is_active}, "
            f"autorenewal={self.autorenewal}, start_date={self.start_date}, end_date={self.end_date})"
        )

class SubscriptionDAO(BaseDAO):
    model = Subscription()
     
class SubsPattern(BaseModel):
    id: int = Field(..., description="")
    user_id: int = Field(..., description="")
    is_active: bool = Field(..., description="")
    autorenewal: bool = Field(..., description="")
    period: int = Field(..., description="")
    start_date: date = Field(..., description="")
    end_date: date = Field(..., description="")

class SubRenewPattern(BaseModel):
    user_id: int = Field(..., description="")
    period: int = Field(..., description="")
    autorenewal: bool = Field(..., description="")
    additional_period: int = Field(..., description="")

class JwtToken(BaseModel):
    id: int = Field(...)
    has_sub: bool = Field(...)
    name: str = Field(...)
    is_admin: bool = Field(...)
