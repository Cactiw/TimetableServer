
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.sql import and_, not_
from sqlalchemy.orm import Session

from model.Pair import Pair, PairOutModel, PairOutWithChangesModel
from model.PeopleUnion import PeopleUnion
from model.User import User
from model.Auditorium import Auditorium

from database import get_db
from service.auth import get_current_user

from service.globals import app


@app.get("/pairs")
def get_pairs(db: Session = Depends(get_db)):
    return db.query(Pair).all()


@app.get("/pairs/by_group/{group_id}", response_model=List[PairOutWithChangesModel])
def get_pairs(group_id: int, db: Session = Depends(get_db)) -> List[PairOutModel]:
    return db.query(Pair).filter_by(group_id=group_id).all()


@app.get("/pairs/by_group/all/{group_id}", response_model=List[PairOutWithChangesModel])
def get_all_pairs(group_id: int, db: Session = Depends(get_db)) -> List[PairOutWithChangesModel]:
    group: PeopleUnion = db.query(PeopleUnion).get(group_id)
    result = []
    while group is not None:
        result += db.query(Pair).filter(Pair.group_id == group.id, not_(Pair.is_canceled.is_(True))).all()
        group = group.parent
    return result


def get_teacher_pairs(user: User, db: Session = Depends(get_db)) -> List[PairOutWithChangesModel]:
    return db.query(Pair).filter(Pair.teacher == user, not_(Pair.is_canceled.is_(True))).all()


@app.get("/pairs/timetable", response_model=List[PairOutWithChangesModel])
def get_timetable(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role == user.STUDENT:
        return get_all_pairs(user.group_id, db)
    elif user.role == user.TEACHER:
        return get_teacher_pairs(user, db)

