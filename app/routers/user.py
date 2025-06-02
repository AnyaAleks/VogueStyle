from typing import Annotated
from fastapi import APIRouter, Path
from dto.user_schema import UserCreate, UserGet, UserUpdate, UserLink
from dao.user import create_user, get_all_users, get_user_by_id, link_telegram_user, update_user, get_user_by_tg_id, get_user_by_phone
from .depends import AsyncSessionDep

router = APIRouter(
    prefix="/user",
    tags=["Все, что связано с пользователем"]
)

@router.post("", response_model=dict, name="Добавление пользователя")
async def post_create_user(
    user_data: UserCreate,
    session: AsyncSessionDep
):
    return await create_user(user_data, session)

@router.get("/tg_id/{user_tg_id}", response_model=dict, name="Получение пользователя по tg_id")
async def get_user_by_tg(
    user_tg_id: Annotated[int, Path(ge=1)],
    session: AsyncSessionDep
):
    result = await get_user_by_tg_id(user_tg_id, session)
    return result

@router.get("/phone/{phone}", response_model=dict, name="Получение пользователя по номеру телефона")
async def get_user_byphone(
    phone: str,
    session: AsyncSessionDep
):
    return await get_user_by_phone(phone, session)

@router.get("", response_model=list[UserGet], name="Получение всех пользователей")
async def get_all_user(
    session: AsyncSessionDep
):
    return await get_all_users(session)

@router.get("/id/{user_id}", response_model=dict, name="Получение пользователя по id")
async def get_user(
    user_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSessionDep
):
    result = await get_user_by_id(user_id, session)
    return result

@router.put("/id/{user_id}", response_model=dict, name="Обновление данных о пользователе")
async def put_update_user(
    user_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    user_data: UserUpdate,
    session: AsyncSessionDep
):
    return await update_user(user_id, user_data, session)

@router.put("/link", response_model=dict, name="Привязка тг по id")
async def put_link_user(
    link_data: UserLink,
    session: AsyncSessionDep
):
    return await link_telegram_user(link_data.phone, link_data.tg_id, session)