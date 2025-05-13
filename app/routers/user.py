from typing import Annotated
from .depends import AsyncSessionDep
from fastapi import APIRouter, Path
from dto.user_schema import UserSchemaCreate, UserSchemaCheck, UserSchemaLink
from dao.user import _get_user_by_id, _create_user, _get_user_by_tg_id, _check_user, _link_user

router = APIRouter(
    prefix="/user",
    tags=["Все, что связано с пользователем"]
)

@router.post("", name="Добавление пользователя")
async def create_user(UserInfo: UserSchemaCreate, session: AsyncSessionDep):
    return await _create_user(UserInfo, session)

@router.get("/tg_id/{user_tg_id}", name="Получение пользователя по tg_id")
async def get_user_by_tg(user_tg_id: int, session: AsyncSessionDep):
    return await _get_user_by_tg_id(user_tg_id, session)

@router.get("/id/{user_id}", name="Получение пользователя по id")
async def get_user_by_id(user_id: Annotated[int, Path(ge=1, lt=1_000_000)], session: AsyncSessionDep):
    return await _get_user_by_id(user_id, session)

@router.post("/check", name="Проверка пользователя")
async def check_user(UserInfo: UserSchemaCheck, session: AsyncSessionDep):
    return await _check_user(UserInfo.phone, UserInfo.password, session)

@router.put("/link", name="Привязка тг по id")
async def link_user(UserInfo: UserSchemaLink, session: AsyncSessionDep):
    return await _link_user(UserInfo, session)