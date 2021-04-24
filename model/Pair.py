
from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Table, text
from sqlalchemy.orm import relationship

from pydantic import BaseModel

from typing import List, Optional

import datetime

from database import Base

from model.User import UserOutModel
from model.Auditorium import AuditoriumOutModel


metadata = Base.metadata


class PairModel(BaseModel):
    begin_time: datetime.datetime
    end_time: datetime.datetime
    subject: str

    class Config:
        orm_mode = True


class PairOutModel(PairModel):
    id: int
    teacher: UserOutModel
    auditorium: Optional[AuditoriumOutModel]
    day_of_week: int
    # pair_to_change: List['PairOutModel'] = []


class Pair(Base):
    __tablename__ = 'pair'

    id = Column(Integer, primary_key=True)
    begin_time = Column(DateTime)
    end_time = Column(DateTime)
    repeatability = Column(Integer, server_default=text("0"))
    subject = Column(String(255))
    auditorium_id = Column(ForeignKey('auditorium.id'))
    pair_to_change_id = Column(ForeignKey('pair.id'))
    teacher_id = Column(ForeignKey('users.id'))
    group_id = Column(ForeignKey('people_union.id'))
    pair_time_pattern = Column(String(255))

    auditorium = relationship('Auditorium')
    group = relationship('PeopleUnion')
    pair_to_change = relationship('Pair', remote_side=[id])
    teacher = relationship('User')

    @property
    def day_of_week(self) -> int:
        return self.begin_time.weekday()
