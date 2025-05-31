# certificate_router.py

from typing import Annotated
from fastapi import APIRouter, Path
from dto.certificate_schema import CertificateCreate, CertificateGet, CertificateUpdate
from dao.certificate import (
    create_certificate,
    get_certificate_by_id,
    get_all_certificates,
    update_certificate,
    delete_certificate
)
from .depends import AsyncSessionDep

router = APIRouter(
    prefix="/certificates",
    tags=["Все, что связано с сертификатами"]
)

@router.post("", response_model=dict, name="Создание сертификата")
async def post_create_certificate(
    cert_data: CertificateCreate,
    session: AsyncSessionDep
):
    """
    Создает новый сертификат на основе переданных данных.
    Возвращает словарь с ключами "ok" и "certificate_id" или ошибкой в случае неудачи.
    """
    return await create_certificate(cert_data, session)


@router.get("/id/{certificate_id}", response_model=dict, name="Получение сертификата по id")
async def get_certificate(
    certificate_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSessionDep
):
    """
    Получает сертификат по его ID.
    Если сертификат существует, возвращает {"ok": True, "certificate": CertificateGet}, иначе {"ok": False, "message": "..."}.
    """
    return await get_certificate_by_id(certificate_id, session)


@router.get("", response_model=list[CertificateGet], name="Получение всех сертификатов")
async def list_certificates(
    session: AsyncSessionDep
):
    """
    Возвращает список всех сертификатов в виде объектов CertificateGet.
    """
    return await get_all_certificates(session)


@router.put("/id/{certificate_id}", response_model=dict, name="Обновление сертификата")
async def put_update_certificate(
    certificate_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    cert_data: CertificateUpdate,
    session: AsyncSessionDep
):
    """
    Обновляет поля существующего сертификата по его ID.
    При успешном обновлении возвращает {"ok": True, "certificate_id": ...}, иначе возвращает ошибку.
    """
    return await update_certificate(certificate_id, cert_data, session)


@router.delete("/id/{certificate_id}", response_model=dict, name="Удаление сертификата")
async def delete_certificate_endpoint(
    certificate_id: Annotated[int, Path(ge=1, lt=1_000_000)],
    session: AsyncSessionDep
):
    """
    Удаляет сертификат по его ID.
    При успешном удалении возвращает {"ok": True, "message": "Сертификат удалён"}, иначе возвращает ошибку.
    """
    return await delete_certificate(certificate_id, session)
