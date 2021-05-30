
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.sql import and_, not_
from sqlalchemy.orm import Session

from model.User import User
from model.Pair import Pair, CancelPairModel, CancelPairResponseModel
from model.Request import Request, RequestInModel, RequestOutModel, RequestResolveModel

from routes.pairs import cancel_pair

from database import get_db
from service.auth import get_current_user

from service.telegram_service import send_notify

from service.globals import app, NOTIFY_ID

import datetime


@app.post("/requests/create", response_model=RequestOutModel)
def create_request(model: RequestInModel, response: Response, db: Session = Depends(get_db),
                   user: User = Depends(get_current_user)):
    cancel_model = CancelPairModel(pair_id=model.request_pair_id, pair_date=model.change_date)
    response_model: dict = cancel_pair(cancel_model, response, db, user, delete_canceled=False)
    canceled_data: Pair = response_model.get("cancel_data")
    request = Request(
        new_begin_time=model.new_begin_time, new_end_time=model.new_end_time, change_date=model.change_date,
        request_pair_id=model.request_pair_id, change_pair_id=canceled_data.id
    )
    db.add(request)
    db.commit()

    send_notify(NOTIFY_ID, "Занятие \"<b>{}</b>\" {} не состоится и будет перенесено.".format(
        canceled_data.subject, canceled_data.russian_begin_time
    ))

    return request


@app.post("/requests/resolve")
def resolve_request(model: RequestResolveModel, db: Session = Depends(get_db)):
    request: Request = db.query(Request).get(model.request_id)
    if not request:
        raise HTTPException(404, "Request not found!")
    if request.processed:
        raise HTTPException(409, "Request already resolved!")
    request.processed = True
    request.processed_at = datetime.datetime.now()
    request.auditorium_id = model.auditorium_id

    change: Pair = request.change_pair
    change.begin_time = request.new_begin_time
    change.end_time = request.new_end_time
    change.is_canceled = False

    db.add(request)
    db.add(change)
    db.commit()

    send_notify(NOTIFY_ID, "Занятие \"<b>{}</b>\" {} перенесено на {}.".format(
        change.subject, change.pair_to_change.russian_begin_time, change.russian_begin_time
    ))

    return {"ok": True, "result": "Request resolved!"}
