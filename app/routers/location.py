# location_router.py

from typing import Annotated
from fastapi import APIRouter, Path
from dto.location_schema import LocationCreate, LocationGet, LocationUpdate
from dto.master_schema import MasterGet
from dao.location import (
    create_location,
    get_location_by_id,
    get_all_locations,
    update_location,
    delete_location,
    get_masters_by_location_id
)
from .depends import AsyncSessionDep

router = APIRouter(
    prefix="/locations",
    tags=["Все, что связано с локациями"]
)

@router.post("", response_model=dict, name="Создание локации")
async def post_create_location(
    location_data: LocationCreate,
    session: AsyncSessionDep
):
    """
    Создает новую локацию на основе переданных данных.
    Возвращает словарь с ключами "ok" и "location_id" или ошибкой в случае неудачи.
    """
    return await create_location(location_data, session)


@router.get("/id/{location_id}", response_model=dict, name="Получение локации по id")
async def get_location(
    location_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSessionDep
):
    """
    Получает локацию по её ID.
    Если локация существует, возвращает {"ok": True, "location": LocationGet}, иначе {"ok": False, "message": "..."}.
    """
    return await get_location_by_id(location_id, session)


@router.get("", response_model=list[LocationGet], name="Получение всех локаций")
async def list_locations(
    session: AsyncSessionDep
):
    """
    Возвращает список всех локаций в виде объектов LocationGet.
    """
    return await get_all_locations(session)


@router.put("/id/{location_id}", response_model=dict, name="Обновление локации")
async def put_update_location(
    location_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    location_data: LocationUpdate,
    session: AsyncSessionDep
):
    """
    Обновляет поля существующей локации по её ID.
    При успешном обновлении возвращает {"ok": True, "location_id": ...}, иначе возвращает ошибку.
    """
    return await update_location(location_id, location_data, session)


@router.delete("/id/{location_id}", response_model=dict, name="Удаление локации")
async def delete_location_endpoint(
    location_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSessionDep
):
    """
    Удаляет локацию по её ID.
    При успешном удалении возвращает {"ok": True, "message": "Локация удалена"}, иначе возвращает ошибку.
    """
    return await delete_location(location_id, session)


@router.get("/id/{location_id}/masters", response_model=list[MasterGet], name="Получение мастеров по локации")
async def get_masters_by_location(
    location_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSessionDep
):
    """
    Возвращает список мастеров (MasterGet) для заданной локации по её ID.
    """
    return await get_masters_by_location_id(location_id, session)
