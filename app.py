
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from model.models import Pair

from database import SessionMaker

import uvicorn


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


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=6000, log_level="info")
