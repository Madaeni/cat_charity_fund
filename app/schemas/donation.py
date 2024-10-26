from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from core.constants import FULL_AMOUNT_GREATER_THAN


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: Optional[int]


class DonationCreate(DonationBase):
    full_amount: int = Field(gt=FULL_AMOUNT_GREATER_THAN)


class DonationDB(DonationBase):
    id: int
    fully_invested: Optional[bool]
    invested_amount: Optional[int]
    close_date: Optional[datetime]
    create_date: datetime
    user_id: Optional[int]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
