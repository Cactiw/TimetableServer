
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.sql import and_, not_
from sqlalchemy.orm import Session

from model.User import User
from model.Pair import Pair, CancelPairModel, CancelPairResponseModel
from model.Request import Request, RequestInModel, RequestOutModel

from routes.pairs import cancel_pair

from database import get_db
from service.auth import get_current_user

from service.globals import app


@app.post("/requests/create", response_model=RequestOutModel)
def create_request(model: RequestInModel, response: Response, db: Session = Depends(get_db),
                   user: User = Depends(get_current_user)):
    cancel_model = CancelPairModel(pair_id=model.request_pair_id, pair_date=model.change_date)
    response_model: dict = cancel_pair(cancel_model, response, db, user, delete_canceled=False)
    print(response_model)
    request = Request(
        new_begin_time=model.new_begin_time, new_end_time=model.new_end_time, change_date=model.change_date,
        request_pair_id=model.request_pair_id, change_pair_id=response_model.get("cancel_data").id
    )
    db.add(request)
    db.commit()
    return request


