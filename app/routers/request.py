from typing import Annotated
from fastapi import APIRouter, Path
from dto.request_schema import RequestCreate, RequestGet, RequestUpdate
from dao.request import create_request, delete_request, update_request, get_request_by_id, get_all_requests, get_all_actual_requests
from .depends import AsyncSessionDep

router = APIRouter(
    prefix="/requests",
    tags=["Все, что связано с заявками"]
)

@router.post("", response_model=dict, name="Создание заявки")
async def post_create_request(
    request_data: RequestCreate,
    session: AsyncSessionDep
):
    return await create_request(request_data, session)

@router.put("/id/{request_id}", response_model=dict, name="Обновление данных заявки")
async def put_update_request(
    request_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    request_data: RequestUpdate,
    session: AsyncSessionDep
):
    return await update_request(request_id, request_data, session)

@router.get("/id/{request_id}", response_model=dict, name="Получение заявки по id")
async def get_request(
    request_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSessionDep
):
    return await get_request_by_id(request_id, session)

@router.get("/actual", response_model=list[RequestGet], name="Получение всех актуальных записей")
async def list_actual_requests(
    session: AsyncSessionDep
):
    return await get_all_actual_requests(session)

@router.get("", response_model=list[RequestGet], name="Получение всех записей")
async def list_requests(
    session: AsyncSessionDep
):
    return await get_all_requests(session)

@router.delete("/id/{request_id}", response_model=dict, name="Удаление записи")
async def delete_request_endpoint(
    request_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSessionDep
):
    return await delete_request(request_id, session)