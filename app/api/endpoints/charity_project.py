from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import (
    check_project_exists,
    check_name_duplicate,
    check_project_invested,
    check_project_full_invested,
    check_correct_project_full_amount,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud, donation_crud
from app.schemas import (
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDB
)


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_meeting_room(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    from_objs = await donation_crud.get_opened(session)
    new_project = await charity_project_crud.create(
        obj_in=charity_project,
        session=session,
    )
    if from_objs:
        modified = charity_project_crud.invest(
            target=new_project, sources=from_objs
        )
        await charity_project_crud.bulk_update(
            sources=modified, session=session
        )
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_meeting_rooms(
        session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_meeting_room(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exists(
        project_id, session
    )
    await check_project_full_invested(
        project
    )
    if obj_in.full_amount:
        await check_correct_project_full_amount(
            project, obj_in.full_amount
        )
    if obj_in.name and project.name != obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    project = await charity_project_crud.update(
        project, obj_in, session
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_meeting_room(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exists(project_id, session)
    await check_project_invested(
        project
    )
    project = await charity_project_crud.remove(project, session)
    return project
