from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from dto.master_schema import MasterSchemaCreate, MasterSchemaGet
from models.master_model import MasterModel
from sqlalchemy import select
# from sqlalchemy.orm import selectinload

async def _create_master(MasterInfo: MasterSchemaCreate, session: AsyncSession):
    master = MasterModel(
        name = MasterInfo.name,
        surname = MasterInfo.surname,
        patronymic = MasterInfo.patronymic,
        password = MasterInfo.password,
        phone = MasterInfo.phone
    )
    
    try:
        session.add(master)
        await session.commit()
    except Exception:
        return {"ok": False, "message":"Ошибка при добавлении нового мастера"}
    return {"ok": True, "message":"Мастер успешно добавлен"}

async def _get_master_by_id(master_id: int, session: AsyncSession):
    master = None
    
    try:
        # stmt = select(MasterModel).options(selectinload(MasterModel.requests)).where(MasterModel.id == master_id) <- это позволяет получить еще все записи связанные с нужным мастром
        stmt = select(MasterModel).where(MasterModel.id == master_id)
        result = await session.execute(stmt)
        master: MasterModel = result.scalar_one()
    except Exception as e:
        print(e)
        return {"ok": False, "message":"Ошибка при попытке полуения мастера"}
    return {"ok": True, "master": MasterSchemaGet(id=master.id, name=master.name, surname=master.surname, patronymic=master.patronymic, phone=master.phone)}

async def _get_all_masters(session: AsyncSession):
    masters = []
    try:
        stmt = select(MasterModel.id, MasterModel.name, MasterModel.surname, MasterModel.patronymic, MasterModel.phone)
        result = await session.execute(stmt)
        data: list[MasterModel] = result.all()
        for row in data:
            masters.append(MasterSchemaGet(id=row.id, name=row.name, surname=row.surname, patronymic=row.patronymic, phone=row.phone))
    except Exception as e:
        print(e)
        return {"ok": False, "message":"Ошибка при попытке полуения мастера"}
    return {"ok": True, "masters": masters}
        
async def _check_master(phone: str, password: str, session: AsyncSession):
    try:
        stmt = select(MasterModel).where(MasterModel.phone==phone)
        result = await session.execute(stmt)
        master: MasterModel = result.scalar_one()
        if master.verify_password(password):
            return {"ok": True, "verified": True, "message":"Данные подтверждены"}
        else:
            return {"ok": True, "verified": False, "message":"Данные не подтверждены"}
    except NoResultFound:
        return {"ok": False, "verified": False, "message":"Неверные данные"}
    except Exception as e:
        return {"ok": False, "verified": False, "message":f"Непредвиденая ошибка при проверке пользователя: {e}"}
    