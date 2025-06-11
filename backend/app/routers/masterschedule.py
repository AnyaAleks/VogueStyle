from typing import Annotated
from fastapi import APIRouter, Path
from dto.masterschedule_schema import (
    MasterScheduleCreate,
    MasterScheduleUpdate,
    MasterScheduleGet
)
from dao.masterschedule import (
    create_master_schedule,
    get_master_schedule_by_id,
    get_all_master_schedules,
    update_master_schedule,
    delete_master_schedule
)
from .depends import AsyncSessionDep

router = APIRouter(
    prefix="/master-schedules",
    tags=["Все, что связано с расписанием мастеров"]
)

@router.post("", response_model=dict, name="Создание расписания мастера")
async def post_create_master_schedule(
    schedule_data: MasterScheduleCreate,
    session: AsyncSessionDep
):
    return await create_master_schedule(schedule_data, session)


@router.get("/id/{master_id}", response_model=dict, name="Получение расписания по id мастера")
async def get_master_schedule(
    master_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSessionDep
):
    return await get_master_schedule_by_id(master_id, session)


@router.get("", response_model=list[MasterScheduleGet], name="Получение всех расписаний")
async def list_master_schedules(
    session: AsyncSessionDep
):
    return await get_all_master_schedules(session)


@router.put("/id/{schedule_id}", response_model=dict, name="Обновление расписания")
async def put_update_master_schedule(
    schedule_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    schedule_data: MasterScheduleUpdate,
    session: AsyncSessionDep
):
    return await update_master_schedule(schedule_id, schedule_data, session)


@router.delete("/id/{schedule_id}", response_model=dict, name="Удаление расписания")
async def delete_master_schedule_endpoint(
    schedule_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSessionDep
):
    return await delete_master_schedule(schedule_id, session)