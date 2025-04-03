from fastapi import APIRouter, HTTPException
from dto.request_schema import RequestSchemaCreate
from services.request_services import _create_request
from .depends import AsyncSessionDep

router = APIRouter(
    prefix="/requests",
    tags=["Все, что связано с заявками"]
)

@router.post("", name="Создание заявки")
async def create_request(RequestInfo: RequestSchemaCreate, session: AsyncSessionDep):
    return await _create_request(RequestInfo, session)