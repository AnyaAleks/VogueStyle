from fastapi import APIRouter
from dao.tg import get_all_roles, get_tg_role, set_tg_role, create_tg_role, delete_role_by_id, get_all_tgs_by_role
from .depends import AsyncSessionDep

router = APIRouter(
    prefix="/tg",
    tags=["Все, что связано с tg"]
)

@router.get("/all",name="Получить все роли")
async def get_allroles(session: AsyncSessionDep):
    return await get_all_roles(session)

@router.get("/all/{role}",name="Получить все тг по роли")
async def get_alltgs(role:int, session: AsyncSessionDep):
    return await get_all_tgs_by_role(role, session)

@router.get("/{tg_id}",name="Получить роль по tg id")
async def get_role(tg_id: int, session: AsyncSessionDep):
    return await get_tg_role(tg_id, session)

@router.put("/{tg_id}", name="Установка роли по tg id")
async def set_role(tg_id: int, role:int, session: AsyncSessionDep):
    return await set_tg_role(tg_id, role, session)

@router.post("/{tg_id}", name="Создание новой записи для tg")
async def create_role(tg_id: int, role:int, session:AsyncSessionDep):
    return await create_tg_role(tg_id, role, session)

@router.delete("/{id}", name="Удаление записи для tg")
async def delete_role(id: int, role:int, session:AsyncSessionDep):
    return await delete_role_by_id(id, session)
