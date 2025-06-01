from typing import Annotated
from fastapi import APIRouter, Path
from dto.service_schema import ServiceCreate, ServiceGet, ServiceUpdate
from dao.service import get_all_services, create_service, update_service, get_service_by_id
from .depends import AsyncSessionDep

router = APIRouter(
    prefix="/services",
    tags=["Все, что связано с услугами"]
)

@router.post("", response_model=dict, name="Создание услуги")
async def post_create_service(
    service_data: ServiceCreate,
    session: AsyncSessionDep
):
    return await create_service(service_data, session)

@router.get("/id/{service_id}", response_model=dict, name="Получение услуги по id")
async def get_service(
    service_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSessionDep
):
    result = await get_service_by_id(service_id, session)
    return result

@router.get("", response_model=dict, name="Получение всех услуг")
async def list_services(
    session: AsyncSessionDep
):
    return await get_all_services(session)

@router.put("/id/{service_id}", response_model=dict, name="Обновление данных о услуге")
async def put_update_service(
    service_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    service_data: ServiceUpdate,
    session: AsyncSessionDep
):
    return await update_service(service_id, service_data, session)

@router.delete("/id/{service_id}", response_model=dict, name="Удаление услуги")
async def delete_service(
    service_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSessionDep
):
    return await delete_service(service_id, session)