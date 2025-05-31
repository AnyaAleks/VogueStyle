from sqlalchemy import Time, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from .base_model import Base

class MasterScheduleModel(Base):
    __tablename__ = "master_schedules"

    master_id: Mapped[int] = mapped_column(ForeignKey("masters.id"))
    weekday: Mapped[int]  # 0 = Monday, 6 = Sunday
    start_time: Mapped[Time]
    end_time: Mapped[Time]
    
    @validates("weekday")
    def validate_weekday(self, key, value):
        if not 0 <= value <= 6:
            raise ValueError("День недели может быть: 0(пн)-6(вс)")
        return value