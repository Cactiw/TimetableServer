from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from model.PeopleUnion import PeopleUnion, PeopleUnionOutModel
from service.globals import app
from model.User import User
from service.auth import get_current_user, get_current_operator_user


@app.get('/groups/searchGroup', response_model=List[PeopleUnionOutModel])
async def search_group(q: str, db: Session = Depends(get_db), user: User = Depends(get_current_operator_user)):
    return db.query(PeopleUnion).filter(PeopleUnion.name.ilike(
            f'%{q.lower().strip()}%'
        )
    ).limit(15).all()
