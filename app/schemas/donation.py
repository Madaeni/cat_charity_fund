from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: Optional[int]


class DonationCreate(DonationBase):
    full_amount: int = Field(..., gt=0)


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
