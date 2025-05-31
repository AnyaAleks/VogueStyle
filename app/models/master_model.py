from __future__ import annotations
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String, ForeignKey
from passlib.context import CryptContext

from .base_model import Base
# Здесь мы всё ещё можем импортировать LocationModel «боевым» путём,
# потому что у LocationModel уже нет прямого импорта MasterModel
from .location_model import LocationModel

# Но для других моделей (RequestModel, ServiceModel, CertificateModel) рекомендуется использовать строковые связи.
PASSLIB_CONTEXT = CryptContext(
    schemes=["pbkdf2_sha512"],
    deprecated="auto"
)

class MasterModel(Base):
    __tablename__ = "masters"

    # Если мы хотим, чтобы SQLAlchemy знала, какие поля создавать, а IDE понимал тип, 
    # можно писать List["RequestModel"], не импортируя RequestModel напрямую.
    requests: Mapped[List["RequestModel"]] = relationship("RequestModel", back_populates="master")
    certificates: Mapped[List["CertificateModel"]] = relationship("CertificateModel", back_populates="master")
    services: Mapped[List["ServiceModel"]] = relationship("ServiceModel", back_populates="master")

    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    # Здесь можно указывать полноценный класс LocationModel, потому что LocationModel не импортирует этот модуль в ответ
    location: Mapped[LocationModel] = relationship("LocationModel", back_populates="masters")

    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    patronymic: Mapped[str] = mapped_column(nullable=True)
    job: Mapped[str] = mapped_column(nullable=True)
    specialization: Mapped[str] = mapped_column(nullable=True)
    experience: Mapped[int] = mapped_column(nullable=True)
    education: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(String(11), nullable=False)
    email: Mapped[str] = mapped_column(nullable=True)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    photo_link: Mapped[str] = mapped_column(nullable=True)

    def __init__(self, password=None, password_hash=None, **kwargs):
        if password_hash is None and password is not None:
            password_hash = self.generate_hash(password)
        super().__init__(password_hash=password_hash, **kwargs)

    @validates("experience")
    def validate_experience(self, key, value):
        if not 0 < value < 100:
            raise ValueError(f"Invalid experience: {value}")
        return value

    @property
    def password(self):
        raise AttributeError("User.password is write-only")

    @password.setter
    def password(self, password):
        self.password_hash = self.generate_hash(password)

    def verify_password(self, password):
        return PASSLIB_CONTEXT.verify(password, self.password_hash)

    @staticmethod
    def generate_hash(password):
        """Generate a secure password hash from a new password"""
        return PASSLIB_CONTEXT.hash(password.encode("utf8"))
