from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User,
    ):
        db_objs = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return db_objs.scalars().all()

    async def not_distributed_donations(
        self,
        session: AsyncSession,
    ):
        projects = await session.execute(
            select(Donation).where(
                Donation.fully_invested == 0
            ).order_by(Donation.create_date)
        )
        return projects.scalars().all()

    async def get_not_distributed_donations(
        self,
        session: AsyncSession,
    ):
        donations = await session.execute(
            select(Donation).where(
                Donation.fully_invested == 0
            ).order_by(Donation.create_date)
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)