from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
    ):
        obj_in_data = obj_in.dict()
        if user:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_id_by_name(
            self,
            obj_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(self.model.id).where(
                self.model.name == obj_name
            )
        )
        return db_project_id.scalars().first()

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User,
    ):
        db_objs = await session.execute(
            select(self.model).where(self.model.user_id == user.id)
        )
        return db_objs.scalars().all()

    async def get_unfunded(
        self,
        session: AsyncSession,
    ):
        projects = await session.execute(
            select(self.model).where(
                self.model.fully_invested == 0
            ).order_by(self.model.create_date)
        )
        return projects.scalars().all()

    def invest(
        self,
        target,
        sources,
    ):
        modified = []
        remains = target.full_amount
        for source in sources:
            if target.fully_invested:
                break
            if (source.full_amount - source.invested_amount - remains) < 0:
                remains = (
                    remains + source.invested_amount - source.full_amount
                )
                target.invested_amount = target.full_amount - remains
                source.invested_amount = source.full_amount
                source.fully_invested = True
                source.close_date = datetime.now()
            else:
                source.invested_amount += remains
                if source.invested_amount == source.full_amount:
                    source.fully_invested = True
                    source.close_date = datetime.now()
                remains = 0
            if remains == 0:
                target.invested_amount = target.full_amount
                target.fully_invested = True
                target.close_date = datetime.now()
            modified.append(source)
        return modified, target