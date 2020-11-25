
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


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000, log_level="info")
