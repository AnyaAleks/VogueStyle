from .depends import AsyncSessionDep
from fastapi import APIRouter
from dto.user_schema import UserSchemaCreate, UserSchemaCheck
from services.user_services import _create_user, _get_user_by_tg_id, _check_user

router = APIRouter(
    prefix="/user",
    tags=["Все, что связано с пользователем"]
)

@router.post("", name="Добавление пользователя")
async def create_user(UserInfo: UserSchemaCreate, session: AsyncSessionDep):
    return await _create_user(UserInfo, session)

@router.get("/{user_tg_id}", name="Получение пользователя по tg_id")
async def get_user_by_tg(user_tg_id: int, session: AsyncSessionDep):
    return await _get_user_by_tg_id(user_tg_id, session)

@router.post("/check", name="Проверка пользователя")
async def check_user(UserInfo: UserSchemaCheck, session: AsyncSessionDep):
    return await _check_user(UserInfo.phone, UserInfo.password, session)