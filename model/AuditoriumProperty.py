

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Table, text
from sqlalchemy.orm import relationship

from pydantic import BaseModel

import datetime

from database import Base


class AuditoriumPropertyModel(BaseModel):
    name: str

    class Config:
        orm_mode = True


class AuditoriumPropertyOutModel(AuditoriumPropertyModel):
    id: int


class AuditoriumProperty(Base):
    __tablename__ = 'auditorium_property'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
