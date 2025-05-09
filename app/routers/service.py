from typing import Annotated
from fastapi import APIRouter, Path
from dto.service_schema import ServiceSchemaCreate, ServiceSchemaUpdate
from dao.service import _create_service, _get_all_services, _get_service_by_id, _update_service
from .depends import AsyncSessionDep

router = APIRouter(
    prefix="/services",
    tags=["Все, что связано с услугами"]
)

@router.post("", name="Создание услуги")
async def create_service(ServiceInfo: ServiceSchemaCreate, session: AsyncSessionDep):
    return await _create_service(ServiceInfo, session)

@router.get("/id/{service_id}", name="Получение услуги по id")
async def get_service_by_id(service_id: Annotated[int, Path(ge=1, lt=1_000_000)], session: AsyncSessionDep):
    return await _get_service_by_id(service_id, session)

@router.get("", name="Получение всех услуг")
async def get_all_services(session: AsyncSessionDep):
    return await _get_all_services(session)

@router.put("", name="Обновление данных о услуге")
async def update_service(ServiceInfo: ServiceSchemaUpdate, session: AsyncSessionDep):
    return await _update_service(ServiceInfo, session)