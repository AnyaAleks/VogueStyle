from .depends import AsyncSessionDep
from fastapi import APIRouter, Path
from dao.master import _update_master, _create_master, _get_all_masters, _get_master_by_id, _check_master, _update_master_password
from dto.master_schema import MasterSchemaCreate, MasterSchemaCheck, MasterSchemaUpdate, MasterSchemaUpdatePassword
from typing import Annotated

router = APIRouter(
    prefix="/master",
    tags=["Все, что свзяано с мастером"]
    )

@router.post("", name="Добавление мастера")
async def create_master(MasterInfo: MasterSchemaCreate, session: AsyncSessionDep):
    return await _create_master(MasterInfo, session)

@router.get("/id/{master_id}", name="Получение мастера по id")
async def get_master_by_id(master_id: Annotated[int, Path(ge=1, lt=1_000_000)], session: AsyncSessionDep):
    return await _get_master_by_id(master_id, session)

@router.get("", name="Получение всех мастеров")
async def get_all_masters(session: AsyncSessionDep):
    return await _get_all_masters(session)

@router.put("", name="Обновление данных мастера")
async def update_master(MasterInfo: MasterSchemaUpdate, session: AsyncSessionDep):
    return await _update_master(MasterInfo, session)

@router.put("/pass", name="Обновление пароля мастера")
async def update_master_password(MasterInfo: MasterSchemaUpdatePassword, session: AsyncSessionDep):
    return await _update_master_password(MasterInfo, session)

@router.post("/check", name="Проверка мастера")
async def check_master(MasterInfo: MasterSchemaCheck, session: AsyncSessionDep):
    return await _check_master(MasterInfo, session)