# from dto.user_schema import UserSchemaCreate, UserSchemaGet, UserSchemaLink
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from models.user_model import UserModel
from dto.user_schema import UserCreate, UserUpdate, UserGet
from .utility import get_object_by_id

async def create_user(user_data: UserCreate, session: AsyncSession) -> dict:
    user = UserModel(**user_data.model_dump())
    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при добавлении пользователя", "details": str(e)}
    return {"ok": True, "user_id": user.id}

async def update_user(user_id: int, data: UserUpdate, session: AsyncSession) -> dict:
    user = await get_object_by_id(UserModel, user_id, session)
    if not user:
        return {"ok": False, "message": "Пользователь не найден"}
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    try:
        await session.commit()
        await session.refresh(user)
        return {"ok": True, "user_id": user.id}
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при обновлении пользователя", "details": str(e)}

async def get_user_by_id(user_id: int, session: AsyncSession) -> dict:
    """
    Возвращает одного пользователя по ID, включая список ID его запросов (requests).
    """
    result = await session.execute(
        select(UserModel)
        .options(joinedload(UserModel.requests))
        .where(UserModel.id == user_id)
    )
    user: Optional[UserModel] = result.unique().scalar_one_or_none()
    if not user:
        return {"ok": False, "message": "Пользователь не найден"}

    # Собираем список ID запросов
    request_ids: List[int] = [req.id for req in user.requests]

    data = {
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "patronymic": user.patronymic,
        "birthday": user.birthday,
        "tg_id": user.tg_id,
        "phone": user.phone,
        "requests": request_ids
    }

    user_dto = UserGet.model_validate(data)
    return {"ok": True, "user": user_dto}

async def get_user_by_tg_id(tg_id: int, session: AsyncSession) -> dict:
    """
    Возвращает одного пользователя по Telegram ID, включая список ID его запросов (requests).
    """
    try:
        result = await session.execute(
            select(UserModel)
            .options(joinedload(UserModel.requests))
            .where(UserModel.tg_id == tg_id)
        )
        user: Optional[UserModel] = result.unique().scalar_one_or_none()
        if not user:
            return {"ok": False, "message": "Пользователь не найден"}

        request_ids: List[int] = [req.id for req in user.requests]

        data = {
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "patronymic": user.patronymic,
            "birthday": user.birthday,
            "tg_id": user.tg_id,
            "phone": user.phone,
            "requests": request_ids
        }

        user_dto = UserGet.model_validate(data)
        return {"ok": True, "user": user_dto}

    except SQLAlchemyError as e:
        return {
            "ok": False,
            "message": f"Ошибка при попытке получения пользователя по Telegram ID: {e}"
        }

async def get_all_users(session: AsyncSession) -> List[UserGet]:
    """
    Возвращает список всех пользователей с их списками ID запросов (requests).
    """
    result = await session.execute(
        select(UserModel).options(joinedload(UserModel.requests))
    )
    users: List[UserModel] = result.unique().scalars().all()

    output: List[UserGet] = []
    for user in users:
        request_ids: List[int] = [req.id for req in user.requests]

        data = {
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "patronymic": user.patronymic,
            "birthday": user.birthday,
            "tg_id": user.tg_id,
            "phone": user.phone,
            "requests": request_ids
        }

        output.append(UserGet.model_validate(data))

    return output

async def delete_user(user_id: int, session: AsyncSession) -> dict:
    user = await get_object_by_id(UserModel, user_id, session)
    if not user:
        return {"ok": False, "message": "Пользователь не найден"}
    try:
        await session.delete(user)
        await session.commit()
        return {"ok": True, "message": "Пользователь удалён"}
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при удалении", "details": str(e)}
    
async def link_telegram_user(phone: str, tg_id: int, session: AsyncSession) -> dict:
    try:
        result = await session.execute(select(UserModel).where(UserModel.phone == phone))
        user = result.scalar_one_or_none()

        if not user:
            return {"ok": False, "message": f"Пользователь с номером {phone} не найден"}

        # Проверка на повторное связывание
        if user.tg_id is not None and user.tg_id != tg_id:
            return {"ok": False, "message": f"Этот пользователь уже связан с другим tg_id: {user.tg_id}"}

        user.tg_id = tg_id
        await session.commit()
        await session.refresh(user)

        return {
            "ok": True,
            "message": "Telegram ID успешно привязан к пользователю",
            "user_id": user.id,
            "tg_id": user.tg_id
        }

    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при привязке Telegram ID", "details": str(e)}