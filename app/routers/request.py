from fastapi import APIRouter, HTTPException
from schema.request_schema import RequestSchemaCreate
from services.request_services import _create_request
from .depends import AsyncSessionDep

router = APIRouter(
    prefix="/requests"
)

@router.post("")
async def create_request(RequestInfo: RequestSchemaCreate, session: AsyncSessionDep):
    return await _create_request(RequestInfo, session)