from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from dto.certificate_schema import CertificateCreate, CertificateGet, CertificateUpdate
from models.certificate_model import CertificateModel
from .utility import get_object_by_id

async def create_certificate(cert_data: CertificateCreate, session: AsyncSession) -> dict:
    cert = CertificateModel(**cert_data.model_dump())
    try:
        session.add(cert)
        await session.commit()
        await session.refresh(cert)
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при добавлении сертификата", "details": str(e)}
    return {"ok": True, "certificate_id": cert.id}

async def update_certificate(certificate_id: int, data: CertificateUpdate, session: AsyncSession) -> dict:
    cert = await get_object_by_id(CertificateModel, certificate_id, session)
    if not cert:
        return {"ok": False, "message": "Сертификат не найден"}
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(cert, field, value)
    try:
        await session.commit()
        await session.refresh(cert)
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при обновлении сертификата", "details": str(e)}
    return {"ok": True, "certificate_id": cert.id}

async def get_certificate_by_id(certificate_id: int, session: AsyncSession) -> dict:
    cert = await get_object_by_id(CertificateModel, certificate_id, session)
    if not cert:
        return {"ok": False, "message": "Сертификат не найден"}
    return {"ok": True, "certificate": CertificateGet.model_validate(cert)}

async def get_all_certificates(session: AsyncSession) -> list[CertificateGet]:
    result = await session.execute(select(CertificateModel))
    certs = result.scalars().all()
    return [CertificateGet.model_validate(c) for c in certs]

async def delete_certificate(certificate_id: int, session: AsyncSession) -> dict:
    cert = await get_object_by_id(CertificateModel, certificate_id, session)
    if not cert:
        return {"ok": False, "message": "Сертификат не найден"}
    try:
        await session.delete(cert)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при удалении сертификата", "details": str(e)}
    return {"ok": True, "message": "Сертификат удалён"}
