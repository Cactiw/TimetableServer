from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Table, text
from sqlalchemy.orm import relationship

from database import Base


metadata = Base.metadata


class Auditorium(Base):
    __tablename__ = 'auditorium'

    id = Column(Integer, primary_key=True)
    additional = Column(JSON)
    max_students = Column(Integer)
    name = Column(String(255))

    properties = relationship('AuditoriumProperty', secondary='auditorium_properties')


class AuditoriumProperty(Base):
    __tablename__ = 'auditorium_property'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class PeopleUnionType(Base):
    __tablename__ = 'people_union_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    parent_id = Column(ForeignKey('people_union_type.id'))

    parent = relationship('PeopleUnionType', remote_side=[id])


t_auditorium_properties = Table(
    'auditorium_properties', metadata,
    Column('auditoriums_id', ForeignKey('auditorium.id'), primary_key=True, nullable=False),
    Column('properties_id', ForeignKey('auditorium_property.id'), primary_key=True, nullable=False)
)


class PeopleUnion(Base):
    __tablename__ = 'people_union'

    id = Column(Integer, primary_key=True, server_default=text("nextval('people_union_id_seq'::regclass)"))
    name = Column(String(255))
    parent_id = Column(ForeignKey('people_union.id'))
    type_id = Column(ForeignKey('people_union_type.id'))

    parent = relationship('PeopleUnion', remote_side=[id])
    type = relationship('PeopleUnionType')
    users = relationship('User', secondary='people_union_users')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    additional = Column(JSON)
    email = Column(String(255))
    last_name = Column(String(255))
    name = Column(String(255))
    role = Column(Integer)
    settings = Column(JSON)
    sur_name = Column(String(255))
    group_id = Column(ForeignKey('people_union.id'))

    group = relationship('PeopleUnion')


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


t_people_union_users = Table(
    'people_union_users', metadata,
    Column('people_union_id', ForeignKey('people_union.id'), nullable=False),
    Column('users_id', ForeignKey('users.id'), nullable=False, unique=True)
)

