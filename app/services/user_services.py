from dto.user_schema import UserSchemaCreate, UserSchemaGet
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select
from models.user_model import UserModel

async def _create_user(UserInfo: UserSchemaCreate, session: AsyncSession):
    user = UserModel(
        name = UserInfo.name,
        tg_id = UserInfo.tg_id,
        phone = UserInfo.phone,
        password = UserInfo.password
    )
    try:
        session.add(user)
        await session.commit()
    except Exception:
        return {"ok": False, "message": "Ошибка при добавлении нового пользователя"}
    return {"ok": True, "message": "Пользователь успешно добавлен"}

async def _get_user_by_tg_id(tg_id: int, session: AsyncSession):
    user = None
    try:
        stmt = select(UserModel).where(UserModel.tg_id == tg_id)
        result = await session.execute(stmt)
        user: UserModel = result.scalar_one()
    except NoResultFound:
        return {"ok": True, "user": user}
    except Exception as e:
        print(e)
        return {"ok": False, "message": "Ошибка при попытки получения пользователя по TG-id"}
    return {"ok": True, "user": UserSchemaGet(id=user.id, name=user.name, tg_id=user.tg_id, phone=user.phone)}

async def _check_user(phone: str, password: str, session: AsyncSession):
    try:
        stmt = select(UserModel).where(UserModel.phone==phone)
        result = await session.execute(stmt)
        user: UserModel = result.scalar_one()
        if user.verify_password(password):
            return {"ok": True, "verified": True, "message":"Данные подтверждены"}
        else:
            return {"ok": True, "verified": False, "message":"Данные не подтверждены"}
    except NoResultFound:
        return {"ok": False, "verified": False, "message":"Неверные данные"}
    except Exception as e:
        return {"ok": False, "verified": False, "message":f"Непредвиденая ошибка при проверке пользователя: {e}"}
    