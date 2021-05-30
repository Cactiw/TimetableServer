
from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Table, text, Date, BOOLEAN, Sequence, \
    TIMESTAMP, func
from sqlalchemy.orm import relationship

from pydantic import BaseModel

from typing import List, Optional

import datetime

from database import Base

from model.Pair import PairOutModel
from model.Auditorium import AuditoriumOutModel


metadata = Base.metadata


class RequestModel(BaseModel):
    new_begin_time: datetime.datetime
    new_end_time: datetime.datetime

    change_date: datetime.date

    class Config:
        orm_mode = True


class RequestInModel(RequestModel):
    request_pair_id: int


class RequestResolveModel(BaseModel):
    request_id: int
    auditorium_id: int


class RequestOutModel(RequestModel):
    auditorium: Optional[AuditoriumOutModel]
    request_pair: PairOutModel

    processed: bool

    created_at: datetime.datetime
    updated_at: datetime.datetime


class Request(Base):
    __tablename__ = 'request'

    id = Column(Integer, Sequence('hibernate_sequence'), primary_key=True)
    new_begin_time = Column(DateTime)
    new_end_time = Column(DateTime)

    auditorium_id = Column(Integer, ForeignKey("auditorium.id"))
    request_pair_id = Column(Integer, ForeignKey("pair.id"))
    change_pair_id = Column(Integer, ForeignKey("pair.id"))
    change_date = Column(Date)

    auditorium = relationship("Auditorium")
    request_pair = relationship("Pair", foreign_keys=[request_pair_id])
    change_pair = relationship("Pair", foreign_keys=[change_pair_id])

    processed = Column(BOOLEAN, default=False)
    processed_at = Column(TIMESTAMP)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

