
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from model.Pair import Pair, PairOutModel
from model.PeopleUnion import PeopleUnion
from model.User import User
from model.Auditorium import Auditorium

from routes.user import generate_token
from routes.pairs import get_pairs
from routes.requests import create_request
from routes.auditoriums import get_auditoriums
from routes.groups import search_group

from service.parser import parse_xls

from database import get_db, Base, engine
from service.globals import app

import uvicorn
import base64


@app.post('/parseXls')
async def parseXls(request: Request, thread_id: int = 1):
    json = await request.json()
    file = base64.b64decode(json['file'])
    result = parse_xls(file)

    # result = parse_xls(path="examples/test.xls")
    return {"result": "ok", "code": 200, "timetable": result}


def init_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
    uvicorn.run("app:app", host="0.0.0.0", port=33222, log_level="info")
