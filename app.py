
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from model.Pair import Pair, PairOutModel
from model.PeopleUnion import PeopleUnion
from model.User import User
from model.Auditorium import Auditorium

from service.parser import parse_xls

from database import SessionMaker

import uvicorn
import base64


app = FastAPI()


# Dependency
def get_db():
    db = SessionMaker()
    try:
        yield db
    finally:
        db.close()


@app.get("/pairs")
def get_pairs(db: Session = Depends(get_db)):
    return db.query(Pair).all()


@app.get("/pairs/by_group/{group_id}", response_model=List[PairOutModel])
def get_pairs(group_id: int, db: Session = Depends(get_db)) -> List[PairOutModel]:
    return db.query(Pair).filter_by(group_id=group_id).all()


@app.get("/pairs/by_group/all/{group_id}", response_model=List[PairOutModel])
def get_pairs(group_id: int, db: Session = Depends(get_db)) -> List[PairOutModel]:
    group: PeopleUnion = db.query(PeopleUnion).get(group_id)
    result = []
    while group is not None:
        result += db.query(Pair).filter_by(group_id=group.id).all()
        group = group.parent
    return result


@app.post('/parseXls')
async def parseXls(request: Request):
    json = await request.json()
    file = base64.b64decode(json['file'])
    result = parse_xls(file)
    return {"result": "ok", "code": 200, "timetable": result}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=6000, log_level="info")
