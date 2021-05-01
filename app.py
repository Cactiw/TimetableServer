
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from model.Pair import Pair, PairOutModel
from model.PeopleUnion import PeopleUnion
from model.User import User
from model.Auditorium import Auditorium

from routes.user import generate_token
from routes.pairs import get_pairs

from service.parser import parse_xls

from database import get_db
from service.globals import app

import uvicorn
import base64


@app.post('/parseXls')
async def parseXls(request: Request):
    json = await request.json()
    file = base64.b64decode(json['file'])
    result = parse_xls(file)
    return {"result": "ok", "code": 200, "timetable": result}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=6000, log_level="info")
