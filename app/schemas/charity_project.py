from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from app.core.constants import (
    PROJECT_NAME_MIN_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_DESCRIPTION_MIN_LENGTH,
    FULL_AMOUNT_GREATER_THAN
)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=PROJECT_NAME_MIN_LENGTH,
        max_length=PROJECT_NAME_MAX_LENGTH
    )
    description: Optional[str] = Field(
        None,
        min_length=PROJECT_DESCRIPTION_MIN_LENGTH
    )
    full_amount: Optional[int] = Field(
        None,
        gt=FULL_AMOUNT_GREATER_THAN
    )


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        min_length=PROJECT_NAME_MIN_LENGTH,
        max_length=PROJECT_NAME_MAX_LENGTH
    )
    description: str = Field(
        min_length=PROJECT_DESCRIPTION_MIN_LENGTH
    )
    full_amount: int = Field(
        gt=FULL_AMOUNT_GREATER_THAN
    )


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
