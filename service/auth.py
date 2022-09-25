import datetime
from typing import Optional, List

from fastapi import Depends, Request, HTTPException
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from model.User import User, LoginUserModel
from database import get_db
from config import JWT_SECRET

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

from service.globals import app


class AuthSettings(BaseModel):
    authjwt_secret_key: str = JWT_SECRET
    authjwt_token_location: List[str] = ['cookies', 'headers']


@AuthJWT.load_config
def get_config():
    return AuthSettings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"details": exc.message}
    )


async def generate_token(model: LoginUserModel, db: Session = Depends(get_db), auth: AuthJWT = Depends()) -> (str, User):
    user: Optional[User] = await authenticate_user(email=model.email.lower(), password=model.password, db=db)
    return auth.create_access_token(subject=user.id, expires_time=datetime.timedelta(days=30)), user


async def authenticate_user(email: str, password: str, db: Session = Depends(get_db)) -> Optional[User]:
    user: User = db.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(401, "User not found")
    if not user.verify_password(password):
        raise HTTPException(401, "Password mismatch")
    return user


async def get_current_user(auth: AuthJWT = Depends(), db: Session = Depends(get_db)) -> Optional[User]:
    auth.jwt_required()
    current_user = db.query(User).get(auth.get_jwt_subject())
    return current_user
