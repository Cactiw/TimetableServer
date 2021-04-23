
from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Table, text
from sqlalchemy.orm import relationship

from pydantic import BaseModel

from typing import List, Optional

import datetime

from database import Base

from model.AuditoriumProperty import AuditoriumPropertyOutModel


metadata = Base.metadata


class AuditoriumModel(BaseModel):
    name: str
    additional: Optional[dict]
    max_students: int

    class Config:
        orm_mode = True


class AuditoriumOutModel(AuditoriumModel):
    id: int
    properties: List[AuditoriumPropertyOutModel]


class Auditorium(Base):
    __tablename__ = 'auditorium'

    id = Column(Integer, primary_key=True)
    additional = Column(JSON)
    max_students = Column(Integer)
    name = Column(String(255))

    properties = relationship('AuditoriumProperty', secondary='auditorium_properties')


t_auditorium_properties = Table(
    'auditorium_properties', metadata,
    Column('auditoriums_id', ForeignKey('auditorium.id'), primary_key=True, nullable=False),
    Column('properties_id', ForeignKey('auditorium_property.id'), primary_key=True, nullable=False)
)
