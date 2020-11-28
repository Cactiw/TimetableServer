
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from model.models import Pair

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


@app.get("/pairs/by_group/{group_id}")
def get_pairs(group_id: int, db: Session = Depends(get_db)):
    return db.query(Pair).filter_by(group_id=group_id).all()


@app.post('/parseXls')
def parseXls(file: str):
    file = base64.b64decode(file)
    result = parse_xls(file)
    return {"result": "ok", "code": 200, "timetable": result}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=6000, log_level="info")
