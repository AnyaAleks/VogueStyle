from typing import List
from datetime import date, timedelta
import shutil, os, uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from fastapi import UploadFile
from fastapi.responses import FileResponse
from dto.master_schema import \
    MasterCheck, MasterUpdate, MasterCreate, MasterGet, MasterPasswordUpdate
from models.master_model import MasterModel
from models.masterschedule_model import MasterScheduleModel
from models.request_model import RequestModel
from .utility import get_object_by_id
from services.available_slots import get_available_slots
# from sqlalchemy.orm import selectinload

UPLOAD_DIR = "uploads/masters"

async def create_master(master_data: MasterCreate, session: AsyncSession) -> dict:
    master = MasterModel(**master_data.model_dump())
    try:
        session.add(master)
        await session.commit()
        await session.refresh(master)
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": f"Ошибка при добавлении мастера связанная с БД: {e}"}
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
        return {"ok": False, "message": f"Ошибка при обновлении мастера в БД: {e}"}
    

    return {"ok": True, "master_id": master.id}

async def get_master_by_id(master_id: int, session: AsyncSession) -> dict:
    """
    Возвращает одного мастера по ID, включая вложенные списки сертификатов и услуг.
    """
    try:
        result = await session.execute(
            select(MasterModel)
            .options(
                joinedload(MasterModel.certificates),
                joinedload(MasterModel.services),
                joinedload(MasterModel.requests)
                    .joinedload(RequestModel.service),
                joinedload(MasterModel.requests)
                    .joinedload(RequestModel.user)
            )
            .where(MasterModel.id == master_id)
        )
        master: MasterModel | None = result.unique().scalar_one_or_none()
        if not master:
            return {"ok": False, "message": "Мастер не найден"}

        # Валидируем ORM-объект мастер через Pydantic, благодаря вложенным схемам
        master_dto = MasterGet.model_validate(master, from_attributes=True)
        result = await session.execute(select(MasterScheduleModel)
                                       .where(MasterScheduleModel.master_id == master_dto.id)
                                       .order_by(MasterScheduleModel.weekday))
        master_schedule: List[MasterScheduleModel] = result.scalars().all()
        reordered_master_schedule = await replace_part_of_schedule(master_schedule)
        
        date_list = [date.today()+timedelta(days=i) for i in range(0,6)]
        result = await session.execute(select(RequestModel)
                                       .where(func.date(RequestModel.schedule_at)
                                              .in_(date_list),
                                              RequestModel.master_id == master_dto.id))
        requests = result.scalars().all()
        master_dto.available_slots = {}
        for schedule in reordered_master_schedule:
            cleared_requests = []
            dt = None
            for request in requests:
                if request.schedule_at.date().isoweekday()-1 == schedule.weekday:
                    cleared_requests.append(request)
                    dt = request.schedule_at.date()
            master_dto.available_slots[f"{schedule.weekday}"] = await get_available_slots(dt, schedule.start_time, schedule.end_time, cleared_requests, minutes_delta=30)
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
            joinedload(MasterModel.services),
            joinedload(MasterModel.requests)
                    .joinedload(RequestModel.service),
            joinedload(MasterModel.requests)
                    .joinedload(RequestModel.user)
        )
    )
    # Избавляемся от дублирования при joinedload
    masters: List[MasterModel] = result.unique().scalars().all()

    output: List[MasterGet] = []
    for m in masters:   
        master_dto = MasterGet.model_validate(m)
        
        result = await session.execute(select(MasterScheduleModel)
                                       .where(MasterScheduleModel.master_id == master_dto.id)
                                       .order_by(MasterScheduleModel.weekday))
        master_schedule: List[MasterScheduleModel] = result.scalars().all()
        reordered_master_schedule = await replace_part_of_schedule(master_schedule)
        
        date_list = [date.today()+timedelta(days=i) for i in range(0,6)]
        result = await session.execute(select(RequestModel)
                                       .where(func.date(RequestModel.schedule_at)
                                              .in_(date_list),
                                              RequestModel.master_id == master_dto.id))
        requests = result.scalars().all()
        master_dto.available_slots = {}
        for schedule in reordered_master_schedule:
            cleared_requests = []
            dt = None
            for request in requests:
                if request.schedule_at.date().isoweekday()-1 == schedule.weekday:
                    cleared_requests.append(request)
                    dt = request.schedule_at.date()
            master_dto.available_slots[f"{schedule.weekday}"] = await get_available_slots(dt, schedule.start_time, schedule.end_time, cleared_requests, minutes_delta=30)
        output.append(master_dto)

    return output

async def replace_part_of_schedule(master_schedule: List[MasterScheduleModel]) -> List[MasterScheduleModel]:
    d = date.today()
    weekday = d.isoweekday()-1
    counter = 0
    for schedule in master_schedule:
        if weekday == schedule.weekday:
            counter+=1
            break
        counter+=1
    if len(master_schedule) == counter:
        return master_schedule
    return master_schedule[counter:]+master_schedule[:counter-1]

async def set_master_photo(master_id: int, photo: UploadFile, session: AsyncSession) -> dict:
    try:
        result = await session.execute(select(MasterModel).where(MasterModel.id == master_id))
        master = result.scalar_one()
        if photo:
            # Удаление старой фотографии
            if master.photo_link and os.path.exists(master.photo_link):
                try:
                    os.remove(master.photo_link)
                except Exception as e:
                    return {"ok": False, "message": f"Ошибка при удалении старого файла: {e}"}

            # Сохранение новой фотографии
            ext = os.path.splitext(photo.filename)[1]
            filename = f"{uuid.uuid4().hex}_{master.id}{ext}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            os.makedirs(UPLOAD_DIR, exist_ok=True)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(photo.file, buffer)

            master.photo_link = file_path
            await session.commit()
            await session.refresh(master)
            return {"ok": True, "message":f"Мастеру с id:{master_id} была установлена фотография"}
    except NoResultFound:
        return {"ok": False, "message":f"Мастер с id:{master_id} не был найден"}
    except Exception as e:
        return {"ok": False, "message": f"Произошла ошибка при сохранении фотографии: {e}"}
    
async def get_master_photo(master_id: int, session: AsyncSession):
    master: MasterModel = await get_object_by_id(MasterModel, master_id, session)
    if not master.photo_link:
        return {"ok": False, "message": "У мастер не установлена фотография"}
    file_path = master.photo_link
    if not os.path.exists(file_path):
        return {"ok": False, "message": "Перезапишите фото мастера пожалуйста"}
    return FileResponse(file_path, media_type="image/jpeg")
    

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
            return {"ok": True, "verified": True, "master_id":master.id,"message": "Данные подтверждены"}
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