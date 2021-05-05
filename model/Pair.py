
from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Table, text, Date
from sqlalchemy.orm import relationship

from pydantic import BaseModel

from typing import List, Optional

import datetime

from database import Base

from model.User import UserOutModel
from model.Auditorium import AuditoriumOutModel
from model.PeopleUnion import PeopleUnionOutModel


metadata = Base.metadata


class PairModel(BaseModel):
    begin_time: datetime.datetime
    end_time: datetime.datetime
    subject: str

    class Config:
        orm_mode = True


class PairOutModel(PairModel):
    id: int
    teacher: Optional[UserOutModel]
    auditorium: Optional[AuditoriumOutModel]
    group: PeopleUnionOutModel
    day_of_week: int
    begin_clear_time: str
    end_clear_time: str

    change_date: Optional[datetime.date]


class PairOutWithChangesModel(PairOutModel):
    changes: Optional[List['PairOutModel']] = []


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
    change_date = Column(Date)

    auditorium = relationship('Auditorium')
    group = relationship('PeopleUnion')
    pair_to_change = relationship('Pair', remote_side=[id], backref="changes")
    teacher = relationship('User')

    @property
    def day_of_week(self) -> int:
        return self.begin_time.weekday()

    @property
    def begin_clear_time(self) -> str:
        return self.begin_time.strftime("%H:%M")

    @property
    def end_clear_time(self) -> str:
        return self.end_time.strftime("%H:%M")

