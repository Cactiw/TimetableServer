
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


class AuditoriumWithAvailabilityModel(AuditoriumOutModel):
    availability: List


class Auditorium(Base):
    __tablename__ = 'auditorium'

    id = Column(Integer, primary_key=True)
    additional = Column(JSON)
    max_students = Column(Integer)
    name = Column(String(255))

    properties = relationship('AuditoriumProperty', secondary='auditorium_properties')
    pairs = relationship('Pair')

    @property
    def availability(self):
        res = []
        for i in range(6):
            day_availability = []
            res.append(day_availability)
            for j in range(6):
                pair_time = datetime.time(hour=9 + j * 2, minute=0)
                day_availability.append(
                    0 if list(filter(
                        lambda p: p.day_of_week == i and (
                            p.begin_time.time() <= pair_time <= p.end_time.time()
                        ),
                        self.pairs
                    )) else 1
                )
        return res


t_auditorium_properties = Table(
    'auditorium_properties', metadata,
    Column('auditoriums_id', ForeignKey('auditorium.id'), primary_key=True, nullable=False),
    Column('properties_id', ForeignKey('auditorium_property.id'), primary_key=True, nullable=False)
)
