from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.tg_model import TgModel
from .utility import get_object_by_id

async def get_all_roles(session: AsyncSession):
    try:
        result = await session.execute(select(TgModel))
        roles = result.scalars().all()
        cleared_roles = [{"id":role.id,"tg_id":role.tg_id, "role":role.role} for role in roles]
        return {"ok": True, "roles": cleared_roles}
    except Exception as e:
        return {"ok": False, "message":f"Непредвиденная ошибка при попытке получения всех ролей: {e}"}
    
async def delete_role_by_id(id: int, session:AsyncSession):
    try:
        role = await get_object_by_id(TgModel, id, session)
        if role is None:
            return {"ok": False, "message":f"Роли с id:{id} не найдено"}
        session.delete(role)
        session.commit()
        return {"ok": True, "message": f"Пользователь с id:{id} успешно удален"}
    except Exception as e:
        session.rollback()
        return {"ok": False, "message":f"Непредвиденная ошибка при попытке удаления роли: {e}"}

async def create_tg_roled(tg_id: int, role:int, session: AsyncSession):
    try:
        result = await session.execute(select(TgModel).where(TgModel.tg_id == tg_id))
        user: TgModel | None = result.scalar_one_or_none()
        if user is not None:
            return {"ok": False, "meessage": f"Пользователь с tg_id:{tg_id} не найден"}
        user = TgModel(tg_id=tg_id, role=role)
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"ok": True, "message": f"Пользователь с tg_id:{tg_id} и ролью:{role} успешно добавлен"}
    except Exception as e:
        session.rollback()
        return {"ok": False, "meessage": f"непредвиденая ошибка: {e}"}

async def set_tg_role(tg_id: int, role:int, session: AsyncSession):
    try:
        result = await session.execute(select(TgModel).where(TgModel.tg_id == tg_id))
        user: TgModel | None = result.scalar_one_or_none()
        if user is None:
            return {"ok": False, "meessage": f"Пользователь с tg_id:{tg_id} не найден"}
        user.role = role
        session.commit()
        session.refresh(TgModel)
        return {"ok": True, "message": f"Пользователю с tg_id:{tg_id} установлена роль - {role}"}
    except Exception as e:
        session.rollback()
        return {"ok": False, "meessage": f"непредвиденая ошибка: {e}"}
        
async def get_tg_role(tg_id: int, session: AsyncSession):
    try:
        result = await session.execute(select(TgModel).where(TgModel.tg_id == tg_id))
        user: TgModel | None = result.scalar_one_or_none()
        if user is None:
            return {"ok": False, "meessage": f"Пользователь с tg_id:{tg_id} не найден"}
        return {"ok": True, "role": f"{user.role}"}
    except Exception as e:
        return {"ok": False, "meessage": f"непредвиденая ошибка: {e}"}