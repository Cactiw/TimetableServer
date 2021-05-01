

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Table, text
from sqlalchemy.orm import relationship

from passlib.hash import bcrypt

from pydantic import BaseModel

from typing import Optional

from database import Base

from model.PeopleUnion import PeopleUnionOutModel


metadata = Base.metadata


class UserModel(BaseModel):
    email: Optional[str]
    name: str
    last_name: str
    sur_name: str
    role: int

    class Config:
        orm_mode = True


class NewUserModel(UserModel):
    password: str
    clear_password: str


class GeneratePasswordModel(BaseModel):
    email: str


class LoginUserModel(BaseModel):
    email: str
    password: str


class UserOutModel(UserModel):
    id: int
    fullname: str
    group: Optional[PeopleUnionOutModel]


class UserLoggedInModel(UserOutModel):
    token: Optional[str]


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    additional = Column(JSON)
    email = Column(String(255))
    password = Column(String(64))
    clear_password = Column(String(64))  # Always None
    last_name = Column(String(255))
    name = Column(String(255))
    role = Column(Integer)
    settings = Column(JSON)
    sur_name = Column(String(255))
    group_id = Column(ForeignKey('people_union.id'))

    group = relationship('PeopleUnion')

    @property
    def fullname(self) -> str:
        return "{} {}{}".format(self.last_name, self.name, " {}".format(self.sur_name) if self.sur_name else "")

    def set_password(self, password: str):
        self.password = bcrypt.hash(password)

    def verify_password(self, password: str) -> bool:
        if not self.password:
            return False
        return bcrypt.verify(password, self.password)


t_people_union_users = Table(
    'people_union_users', metadata,
    Column('people_union_id', ForeignKey('people_union.id'), nullable=False),
    Column('users_id', ForeignKey('users.id'), nullable=False, unique=True)
)


