from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from model.Auditorium import AuditoriumWithAvailabilityModel, Auditorium
from model.User import User
from service.auth import get_current_user
from service.globals import app


@app.get("/auditoriums/", response_model=List[AuditoriumWithAvailabilityModel])
async def get_auditoriums(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Auditorium).all()

