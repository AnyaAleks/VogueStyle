from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from dto.master_schema import MasterSchemaCheck, MasterSchemaUpdate, MasterSchemaCreate, MasterSchemaGet, MasterSchemaUpdatePassword
from models.master_model import MasterModel
from sqlalchemy import select, update
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
    except Exception as e:
        return {"ok": False, "message":f"Ошибка при добавлении нового мастера: {e}"}
    return {"ok": True, "message":"Мастер успешно добавлен"}

async def _get_master_by_id(master_id: int, session: AsyncSession):
    master = None
    
    try:
        # stmt = select(MasterModel).options(selectinload(MasterModel.requests)).where(MasterModel.id == master_id) <- это позволяет получить еще все записи связанные с нужным мастром
        stmt = select(MasterModel).where(MasterModel.id == master_id)
        result = await session.execute(stmt)
        master: MasterModel = result.scalar_one()
    except Exception as e:
        # print(e)
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
        return {"ok": False, "message":f"Ошибка при попытке полуения мастера - {e}"}
    return {"ok": True, "masters": masters}
        
async def _check_master(MasterInfo: MasterSchemaCheck, session: AsyncSession):
    try:
        stmt = select(MasterModel).where(MasterModel.phone==MasterInfo.phone)
        result = await session.execute(stmt)
        master: MasterModel = result.scalar_one()
        if master.verify_password(MasterInfo.password):
            return {"ok": True, "verified": True, "message":"Данные подтверждены"}
        else:
            return {"ok": True, "verified": False, "message":"Данные не подтверждены"}
    except NoResultFound:
        return {"ok": False, "verified": False, "message":"Неверные данные"}
    except Exception as e:
        return {"ok": False, "verified": False, "message":f"Непредвиденая ошибка при проверке пользователя: {e}"}
    
async def _update_master(MasterInfo: MasterSchemaUpdate, session: AsyncSession):
    try:
        await session.execute(update(MasterModel), [{"id":MasterInfo.id, "phone": MasterInfo.phone, "name": MasterInfo.name, "surname": MasterInfo.surname, "patronymic": MasterInfo.patronymic}])
        await session.commit()
    except Exception as e:
        return {"ok": False, "message": f"При попытке обновления данных мастера была произведена ошибка - {e}"}
    return {"ok": True, "message": "Мастер был успешно обновлен"}

async def _update_master_password(MasterInfo: MasterSchemaUpdatePassword, session: AsyncSession):
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