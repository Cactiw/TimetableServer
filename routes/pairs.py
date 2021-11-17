
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.sql import and_, not_
from sqlalchemy.orm import Session

from model.Pair import Pair, PairOutModel, PairOutWithChangesModel, CancelPairModel, CancelPairResponseModel
from model.PeopleUnion import PeopleUnion
from model.User import User
from model.Auditorium import Auditorium

from database import get_db
from service.auth import get_current_user
from service.optimization import count_timetable_score
from service.telegram_service import send_notify

from service.globals import app, NOTIFY_ID

import datetime


@app.get("/pairs")
def get_pairs(db: Session = Depends(get_db)):
    return db.query(Pair).all()


@app.get("/pairs/count_score")
def get_pairs(db: Session = Depends(get_db)):
    return count_timetable_score(db)


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


@app.get("/pairs/teacher", response_model=List[PairOutWithChangesModel])
def get_teacher_pairs(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> List[PairOutWithChangesModel]:
    return db.query(Pair).filter(Pair.teacher == user, not_(Pair.is_canceled.is_(True))).all()


@app.get("/pairs/timetable", response_model=List[PairOutWithChangesModel])
def get_timetable(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role == user.STUDENT:
        return get_all_pairs(user.group_id, db)
    elif user.role == user.TEACHER:
        return get_teacher_pairs(user, db)


@app.post("/pairs/cancel", response_model=CancelPairResponseModel)
def cancel_pair(model: CancelPairModel, response: Response,
                db: Session = Depends(get_db), user: User = Depends(get_current_user),
                delete_canceled: bool = True):
    if user.role not in frozenset({user.TEACHER, user.OPERATOR}):
        raise HTTPException(403, {"error": "This methods requires additional rights."})
    pair: Pair = db.query(Pair).get(model.pair_id)
    if not pair:
        raise HTTPException(404, {"error": "Pair not found."})
    if user.role == user.TEACHER and pair.teacher != user:
        raise HTTPException(403, {"error": "You can not cancel a class that isn't yours."})
    if pair.begin_time.weekday() != model.pair_date.weekday():
        raise HTTPException(409, {"error": "Cancel date do not match pair date."})
    if pair.is_canceled:
        if not delete_canceled:
            return {"ok": True, "result": "Already canceled!", "cancel_data": pair}
        db.delete(pair)
        db.commit()
        return {"ok": True, "result": "Cancel change deleted!"}
    current_changes = list(filter(lambda change: change.change_date == model.pair_date and change.is_canceled,
                                  pair.changes))
    if current_changes:
        if not delete_canceled:
            return {"ok": True, "result": "Already canceled!", "cancel_data": current_changes[0]}
        db.delete(current_changes[0])
        db.commit()
        response.status_code = 200
        return {"ok": True, "result": "Class cancellation canceled!", "cancel_data": None}
    cancel = pair.cancel_pair(model.pair_date)
    db.add(cancel)
    db.commit()
    if delete_canceled:
        send_notify(NOTIFY_ID, "Занятие \"<b>{}</b>\" {} отменено".format(
            cancel.subject, cancel.russian_begin_time
        ))

    return {"ok": True, "result": "Class canceled!", "cancel_data": cancel}


@app.post("/pairs/makeOnline", response_model=CancelPairResponseModel)
def make_pair_online(model: CancelPairModel, response: Response,
                     db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role not in frozenset({user.TEACHER, user.OPERATOR}):
        raise HTTPException(403, {"error": "This methods requires additional rights."})
    pair: Pair = db.query(Pair).get(model.pair_id)
    if not pair:
        raise HTTPException(404, {"error": "Pair not found."})
    if user.role == user.TEACHER and pair.teacher != user:
        raise HTTPException(403, {"error": "You can not cancel a class that isn't yours."})
    if pair.begin_time.weekday() != model.pair_date.weekday():
        raise HTTPException(409, {"error": "Cancel date do not match pair date."})
    if pair.is_online:
        return {"ok": True, "result": "Already online!", "cancel_data": pair}
    current_changes = list(filter(lambda change: change.change_date == model.pair_date and change.is_online,
                                  pair.changes))
    if current_changes:
        return {"ok": True, "result": "Already canceled!", "cancel_data": current_changes[0]}
    online = pair.make_pair_online(model.pair_date)
    db.add(online)
    db.commit()

    send_notify(NOTIFY_ID, "Занятие \"<b>{}</b>\" {} перенесено на дистанционку.".format(
        online.subject, online.russian_begin_time
    ))

    return {"ok": True, "result": "Class canceled!", "online_data": online}

