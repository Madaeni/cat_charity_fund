from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud import donation_crud, charity_project_crud
from app.models import User
from app.schemas import (
    DonationCreate,
    DonationDB,
)

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude={
        'user_id',
        'close_date',
        'invested_amount',
        'fully_invested'
    },
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    from_objs = await charity_project_crud.get_opened(session)
    new_donation = await donation_crud.create(
        obj_in=donation,
        session=session,
        user=user,
    )
    if from_objs:
        modified = donation_crud.invest(
            target=new_donation, sources=from_objs
        )
        await donation_crud.bulk_update(sources=modified, session=session)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=False,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={
        'user_id',
        'close_date',
        'invested_amount',
        'fully_invested'
    },
)
async def get_my_reservations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех бронирований для текущего пользователя."""
    donations = await donation_crud.get_by_user(
        session=session,
        user=user
    )
    return donations
