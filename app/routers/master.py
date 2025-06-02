from typing import Annotated
from fastapi import APIRouter, Path, File, UploadFile, Depends
from dao.master import \
    create_master, get_all_masters, get_master_by_id, update_master, update_master_password, check_master, set_master_photo, get_master_photo
from dto.master_schema import MasterCheck, MasterCreate, MasterGet, MasterPasswordUpdate, MasterUpdate
from .depends import AsyncSessionDep

router = APIRouter(
    prefix="/master",
    tags=["Все, что свзяано с мастером"]
    )

@router.post("/photo/{master_id}", response_model=dict, name="Установка фото мастера")
async def set_photo(
    master_id: int,
    session: AsyncSessionDep,
    photo: UploadFile = File()
):
    return await set_master_photo(master_id, photo, session)

@router.get("/photo/{master_id}", name="Получение фото мастера")
async def get_photo(
    master_id: int,
    session: AsyncSessionDep,
):
    return await get_master_photo(master_id, session)

@router.post("", response_model=dict, name="Добавление мастера")
async def post_create_master(
    session: AsyncSessionDep,
    master_data: MasterCreate
):
    return await create_master(master_data, session)

@router.get("/id/{master_id}", response_model=dict, name="Получение мастера по id")
async def get_master(
    master_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSessionDep
):
    return await get_master_by_id(master_id, session)

@router.get("", response_model=list[MasterGet], name="Получение всех мастеров")
async def list_masters(
    session: AsyncSessionDep
):
    return await get_all_masters(session)

@router.put("/id/{master_id}", response_model=dict, name="Обновление данных мастера")
async def put_update_master(
    session: AsyncSessionDep,
    master_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    master_data: MasterUpdate
):
    return await update_master(master_id, master_data, session)

@router.put("/password", response_model=dict, name="Обновление пароля мастера")
async def put_update_master_password(
    password_data: MasterPasswordUpdate,
    session: AsyncSessionDep
):
    return await update_master_password(password_data, session)

@router.post("/check", response_model=dict, name="Проверка мастера")
async def post_check_master(
    credentials: MasterCheck,
    session: AsyncSessionDep
):
    return await check_master(credentials, session)