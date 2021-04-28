
from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Table, text
from sqlalchemy.orm import relationship

from pydantic import BaseModel

from typing import Optional

from database import Base

from model.PeopleUnionType import PeopleUnionTypeModel, PeopleUnionTypeOutModel


class PeopleUnionModel(BaseModel):
    name: str
    type: PeopleUnionTypeModel

    class Config:
        orm_mode = True


class PeopleUnionOutModel(PeopleUnionModel):
    id: int
    type: PeopleUnionTypeOutModel
    # parent: Optional['PeopleUnionTypeModel']


class PeopleUnion(Base):
    __tablename__ = 'people_union'

    id = Column(Integer, primary_key=True, server_default=text("nextval('people_union_id_seq'::regclass)"))
    name = Column(String(255))
    parent_id = Column(ForeignKey('people_union.id'))
    type_id = Column(ForeignKey('people_union_type.id'))

    parent = relationship('PeopleUnion', remote_side=[id])
    type = relationship('PeopleUnionType')
    users = relationship('User', secondary='people_union_users')

