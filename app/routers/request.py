from typing import Annotated
from fastapi import APIRouter, Path
from dto.request_schema import RequestSchemaCreate
from dao.request import _get_all_actual_requests, _create_request, _get_request_by_id, _get_all_requests
from .depends import AsyncSessionDep

router = APIRouter(
    prefix="/requests",
    tags=["Все, что связано с заявками"]
)

@router.post("", name="Создание заявки")
async def create_request(RequestInfo: RequestSchemaCreate, session: AsyncSessionDep):
    return await _create_request(RequestInfo, session)

@router.get("/id/{request_id}", name="Получение заявки по id")
async def get_request(request_id: Annotated[int, Path(ge=1, lt=1_000_000)], session: AsyncSessionDep):
    return await _get_request_by_id(request_id, session)

@router.get("/actual", name="Получение всех актуальных записей")
async def get_all_actual_requests(session: AsyncSessionDep):
    return await _get_all_actual_requests(session)

@router.get("", name="Получение всех записей")
async def get_all_requests(session: AsyncSessionDep):
    return await _get_all_requests(session)