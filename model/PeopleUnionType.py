
from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Table, text
from sqlalchemy.orm import relationship

from pydantic import BaseModel

from typing import Optional

from database import Base


metadata = Base.metadata


class PeopleUnionTypeModel(BaseModel):
    name: str

    class Config:
        orm_mode = True


class PeopleUnionTypeOutModel(PeopleUnionTypeModel):
    id: int
    parent: Optional['PeopleUnionTypeOutModel']


class PeopleUnionType(Base):
    __tablename__ = 'people_union_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    parent_id = Column(ForeignKey('people_union_type.id'))

    parent = relationship('PeopleUnionType', remote_side=[id])


