
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from model.Pair import Pair, PairOutModel
from model.PeopleUnion import PeopleUnion
from model.User import User, NewUserModel, LoginUserModel, GeneratePasswordModel, UserLoggedInModel
from model.Auditorium import Auditorium

from service.auth import generate_token

from database import get_db
from service.globals import app

import secrets


@app.post('/users/generatePassword', response_model=NewUserModel)
async def generate_password(model: GeneratePasswordModel, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=model.email.lower()).first()
    if user is None:
        return HTTPException(401, "User not found!")
    new_password = secrets.token_urlsafe(6)
    user.set_password(new_password)
    db.add(user)
    db.commit()
    user.clear_password = new_password
    return user


@app.post('/users/login', response_model=UserLoggedInModel)
async def login(model: LoginUserModel, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    token, user = await generate_token(model, db, auth)
    model = UserLoggedInModel.from_orm(user)
    model.token = token
    return model




