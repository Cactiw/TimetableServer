from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from model.Auditorium import AuditoriumWithAvailabilityModel, Auditorium, AuditoriumOutModel
from model.User import User
from service.auth import get_current_user, get_current_operator_user
from service.globals import app


@app.get("/auditoriums/", response_model=List[AuditoriumWithAvailabilityModel])
async def get_auditoriums(db: Session = Depends(get_db), user: User = Depends(get_current_operator_user)):
    return db.query(Auditorium).all()


@app.get('/auditoriums/searchAuditorium', response_model=List[AuditoriumOutModel])
async def search_auditorium(q: str, db: Session = Depends(get_db), user: User = Depends(get_current_operator_user)):
    return db.query(Auditorium).filter(Auditorium.name.ilike(
            f'%{q.lower().strip()}%'
        )
    ).limit(15).all()

