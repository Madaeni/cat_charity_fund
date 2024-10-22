from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(None, gt=0)


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)


class CharityProjectUpdate(CharityProjectBase):

    @validator('name')
    def name_cannot_be_null(cls, value):
        if not value:
            raise ValueError('Название проекта не может быть пустым!')
        return value

    @validator('description')
    def description_cannot_be_null(cls, value):
        if not value:
            raise ValueError('Описание проекта не может быть пустым!')
        return value

    @validator('full_amount')
    def full_amount_cannot_be_null(cls, value):
        if not value:
            raise ValueError('Нужно указать требуемую сумму!')
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    id: int
    create_date: Optional[datetime]
    close_date: Optional[datetime]
    invested_amount: Optional[int]
    fully_invested: Optional[bool]

    class Config:
        orm_mode = True
