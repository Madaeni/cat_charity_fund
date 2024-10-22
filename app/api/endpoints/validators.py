from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name=project_name,
        session=session
    )
    if project_id:
        raise HTTPException(
            status_code=400,
            detail='Такое имя уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(
        obj_id=project_id,
        session=session,
    )
    if not project:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return project


async def check_project_invested(
        project: CharityProject,
) -> CharityProject:
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='Данный проект не может быть изменен!'
        )
    return project


async def check_project_full_invested(
        project: CharityProject,
) -> CharityProject:
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Данный проект не может быть изменен!'
        )
    return project


async def check_correct_project_full_amount(
        project: CharityProject,
        full_amount: int,
) -> CharityProject:
    if full_amount < project.invested_amount:
        raise HTTPException(
            status_code=422,
            detail='Требуемая сумма не может быть меньше внесенной!'
        )
    return project
