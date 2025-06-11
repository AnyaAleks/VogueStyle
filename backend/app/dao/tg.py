from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.tg_model import TgModel
from .utility import get_object_by_id
from typing import Optional


async def get_all_roles(session: AsyncSession):
    try:
        result = await session.execute(select(TgModel))
        roles = result.scalars().all()
        cleared_roles = [{"id": role.id, "tg_id": role.tg_id, "role": role.role} for role in roles]
        return {"ok": True, "roles": cleared_roles}
    except Exception as e:
        return {"ok": False, "message": f"Непредвиденная ошибка при попытке получения всех ролей: {e}"}
    
async def get_all_tgs_by_role(role: int, session: AsyncSession):
    try:
        result = await session.execute(select(TgModel).where(TgModel.role == role))
        roles = result.scalars().all()
        cleared_roles = [role.tg_id for role in roles]
        return {"ok": True, "tgs": cleared_roles}
    except Exception as e:
        return {"ok": False, "message": f"Непредвиденная ошибка при попытке получения всех ролей: {e}"}


async def delete_role_by_id(id: int, session: AsyncSession):
    try:
        role = await get_object_by_id(TgModel, id, session)
        if role is None:
            return {"ok": False, "message": f"Роль с id:{id} не найдена"}
        session.delete(role)
        await session.commit()
        return {"ok": True, "message": f"Роль с id:{id} успешно удалена"}
    except Exception as e:
        await session.rollback()
        return {"ok": False, "message": f"Непредвиденная ошибка при удалении роли: {e}"}


async def create_tg_role(tg_id: int, role: int, session: AsyncSession):
    try:
        result = await session.execute(select(TgModel).where(TgModel.tg_id == tg_id))
        user: Optional[TgModel] = result.scalar_one_or_none()
        if user is not None:
            return {"ok": False, "message": f"Пользователь с tg_id:{tg_id} уже существует"}

        user = TgModel(tg_id=tg_id, role=role)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return {"ok": True, "message": f"Пользователь с tg_id:{tg_id} и ролью:{role} успешно добавлен"}
    except Exception as e:
        await session.rollback()
        return {"ok": False, "message": f"Непредвиденная ошибка: {e}"}


async def set_tg_role(tg_id: int, role: int, session: AsyncSession):
    try:
        result = await session.execute(select(TgModel).where(TgModel.tg_id == tg_id))
        user: Optional[TgModel] = result.scalar_one_or_none()
        if user is None:
            return {"ok": False, "message": f"Пользователь с tg_id:{tg_id} не найден"}

        user.role = role
        await session.commit()
        await session.refresh(user)
        return {"ok": True, "message": f"Роль пользователя с tg_id:{tg_id} успешно обновлена на {role}"}
    except Exception as e:
        await session.rollback()
        return {"ok": False, "message": f"Непредвиденная ошибка: {e}"}


async def get_tg_role(tg_id: int, session: AsyncSession):
    try:
        result = await session.execute(select(TgModel).where(TgModel.tg_id == tg_id))
        user: Optional[TgModel] = result.scalar_one_or_none()
        if user is None:
            return {"ok": False, "message": f"Пользователь с tg_id:{tg_id} не найден"}
        return {"ok": True, "role": user.role}
    except Exception as e:
        return {"ok": False, "message": f"Непредвиденная ошибка: {e}"}
