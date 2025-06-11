from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.masterschedule_model import MasterScheduleModel
from dto.masterschedule_schema import MasterScheduleCreate, MasterScheduleGet, MasterScheduleUpdate
from .utility import get_object_by_id

async def create_master_schedule(data: MasterScheduleCreate, session: AsyncSession) -> dict:
    try:
        result = await session.execute(select(MasterScheduleModel).where(MasterScheduleModel.master_id == data.master_id, MasterScheduleModel.weekday == data.weekday))
        schedule = result.scalar_one()
        schedule.start_time = data.start_time
        schedule.end_time = data.end_time
        await session.commit()
        await session.refresh(schedule)
        return {"ok": True, "message":f"Расписание было успешно обновлено для master_id: {schedule.master_id}"}
    except NoResultFound:
        try:
            schedule = MasterScheduleModel(**data.model_dump())
            session.add(schedule)
            await session.commit()
            await session.refresh(schedule)
        except SQLAlchemyError as e:
            await session.rollback()
            return {"ok": False, "message": "Ошибка при добавлении расписания", "details": str(e)}
        return {"ok": True, "schedule_id": schedule.id}

async def update_master_schedule(schedule_id: int, data: MasterScheduleUpdate, session: AsyncSession) -> dict:
    schedule = await get_object_by_id(MasterScheduleModel, schedule_id, session)
    if not schedule:
        return {"ok": False, "message": "Расписание не найдено"}
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(schedule, field, value)
    try:
        await session.commit()
        await session.refresh(schedule)
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при обновлении расписания", "details": str(e)}
    return {"ok": True, "schedule_id": schedule.id}

async def get_master_schedule_by_id(master_id: int, session: AsyncSession) -> dict:
    result = await session.execute(select(MasterScheduleModel).where(MasterScheduleModel.master_id == master_id))
    schedules = result.scalars().all()
    if len(schedules) < 1:
        return {"ok": False, "message": "Расписание не найдено"}
    return {"ok": True, "schedules": [MasterScheduleGet.model_validate(schedule) for schedule in schedules]}

async def get_all_master_schedules(session: AsyncSession) -> list[MasterScheduleGet]:
    result = await session.execute(select(MasterScheduleModel))
    schedules = result.scalars().all()
    return [MasterScheduleGet.model_validate(s) for s in schedules]

async def delete_master_schedule(schedule_id: int, session: AsyncSession) -> dict:
    schedule = await get_object_by_id(MasterScheduleModel, schedule_id, session)
    if not schedule:
        return {"ok": False, "message": "Расписание не найдено"}
    try:
        await session.delete(schedule)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при удалении расписания", "details": str(e)}
    return {"ok": True, "message": "Расписание удалено"}