from .depends import AsyncSessionDep
from fastapi import APIRouter
from services.master_services import _create_master
from schema.master_schema import MasterSchemaCreate

router = APIRouter(
    prefix="/master"
    )

@router.post("")
async def create_master(MasterInfo: MasterSchemaCreate, session: AsyncSessionDep):
    return await _create_master(MasterInfo, session)