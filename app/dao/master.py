from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from dto.master_schema import \
    MasterCheck, MasterUpdate, MasterCreate, MasterGet, MasterPasswordUpdate
from dto.certificate_schema import CertificateGet
from models.master_model import MasterModel
from models.certificate_model import CertificateModel
from .utility import get_object_by_id
# from sqlalchemy.orm import selectinload

async def create_master(master_data: MasterCreate, session: AsyncSession) -> dict:
    master = MasterModel(**master_data.model_dump())
    try:
        session.add(master)
        await session.commit()
        await session.refresh(master)
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при добавлении мастера", "details": str(e)}
    return {"ok": True, "master_id": master.id}

async def update_master(master_id: int, data: MasterUpdate, session: AsyncSession) -> dict:
    master = await get_object_by_id(MasterModel, master_id, session)
    if not master:
        return {"ok": False, "message": "Мастер не найден"}
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(master, field, value)
    try:
        await session.commit()
        await session.refresh(master)
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при обновлении мастера", "details": str(e)}
    return {"ok": True, "master_id": master.id}

async def get_master_by_id(master_id: int, session: AsyncSession) -> dict:
    """
    Возвращает одного мастера по ID, включая вложенные списки сертификатов и услуг.
    """
    try:
        result = await session.execute(
            select(MasterModel)
            .options(
                joinedload(MasterModel.certificates),  # подгружаем связанные сертификаты
                joinedload(MasterModel.services)       # подгружаем связанные услуги
            )
            .where(MasterModel.id == master_id)
        )
        master: MasterModel | None = result.unique().scalar_one_or_none()
        if not master:
            return {"ok": False, "message": "Мастер не найден"}

        # Валидируем ORM-объект мастер через Pydantic, благодаря вложенным схемам
        master_dto = MasterGet.model_validate(master, from_attributes=True)
        return {"ok": True, "master": master_dto}

    except SQLAlchemyError as e:
        return {"ok": False, "message": f"Непредвиденная ошибка при попытке получения мастера: {e}"}

async def get_all_masters(session: AsyncSession) -> List[MasterGet]:
    """
    Возвращает список всех мастеров с вложенными сертификатами и услугами.
    """
    result = await session.execute(
        select(MasterModel)
        .options(
            joinedload(MasterModel.certificates),
            joinedload(MasterModel.services)
        )
    )
    # Избавляемся от дублирования при joinedload
    masters: List[MasterModel] = result.unique().scalars().all()

    output: List[MasterGet] = []
    for m in masters:
        master_dto = MasterGet.model_validate(m, from_attributes=True)
        output.append(master_dto)

    return output

async def delete_master(master_id: int, session: AsyncSession) -> dict:
    master = await get_object_by_id(MasterModel, master_id, session)
    if not master:
        return {"ok": False, "message": "Мастер не найден"}
    try:
        await session.delete(master)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при удалении мастера", "details": str(e)}
    return {"ok": True, "message": "Мастер удалён"}
        
async def check_master(master_info: MasterCheck, session: AsyncSession) -> dict:
    """
    Проверяет подлинность мастера по телефону или email + паролю.
    """
    try:
        # Если в phoneemail есть '@', считаем это email, иначе — phone
        if "@" in master_info.phoneemail:
            stmt = select(MasterModel).where(MasterModel.email == master_info.phoneemail)
        else:
            stmt = select(MasterModel).where(MasterModel.phone == master_info.phoneemail)

        result = await session.execute(stmt)
        master: MasterModel = result.scalar_one()  # бросит NoResultFound, если не найден

        if master.verify_password(master_info.password):
            return {"ok": True, "verified": True, "message": "Данные подтверждены"}
        else:
            return {"ok": True, "verified": False, "message": "Данные не подтверждены"}

    except NoResultFound:
        return {"ok": False, "verified": False, "message": "Неверные данные"}
    except Exception as e:
        return {
            "ok": False,
            "verified": False,
            "message": f"Непредвиденная ошибка при проверке пользователя: {e}"
        }

async def update_master_password(MasterInfo: MasterPasswordUpdate, session: AsyncSession):
    try:
        stmt = select(MasterModel).where(MasterModel.phone == MasterInfo.phone)
        result = await session.execute(stmt)
        master: MasterModel = result.scalar_one()
        if master.verify_password(MasterInfo.old_password):
            master.password = MasterInfo.new_password
            await session.commit()
            return {"ok": True, "verified": True, "message": "Пароль был обновлен"}
        else:
            return {"ok": True, "verified": False, "message": "Старый пароль неверен"}
    except Exception as e:
        return {"ok": False, "verified": False, "message":f"Непредвиденая ошибка при проверке пользователя: {e}"}