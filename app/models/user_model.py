from .base_model import Base
from .request_model import RequestModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from passlib.context import CryptContext
from typing import List

PASSLIB_CONTEXT = CryptContext(
    schemes=["pbkdf2_sha512"],
    deprecated="auto"
)

class UserModel(Base):
    __tablename__ = "users"
    
    requests: Mapped[List['RequestModel']] = relationship("RequestModel")
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    tg_id: Mapped[int] = mapped_column(Integer(), nullable=True)
    phone: Mapped[str] = mapped_column(String(11), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    
    def __init__(self, password=None, password_hash=None, **kwargs):
        if password_hash is None and password is not None:
            password_hash = self.generate_hash(password)
        super().__init__(password_hash=password_hash, **kwargs)

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