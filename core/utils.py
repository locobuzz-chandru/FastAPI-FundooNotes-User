from datetime import datetime, timedelta

from fastapi import Security, Depends, HTTPException, Request
from fastapi.security import APIKeyHeader
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models import User
from core import settings
from core.database import get_db


class Hasher:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password):
        return cls.pwd_context.hash(password)


class JWT:
    @staticmethod
    def jwt_encode(payload: dict):
        if 'exp' not in payload:
            payload.update(exp=datetime.utcnow() + timedelta(hours=1), iat=datetime.utcnow())
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def jwt_decode(token):
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except jwt.JWTError as e:
            raise e


api_key = APIKeyHeader(name='Authorization')


def jwt_authorization(request: Request, token: str = Security(api_key), db: Session = Depends(get_db)):
    decode_token = JWT.jwt_decode(token)
    user_id = decode_token.get('user')
    user = db.query(User).filter_by(id=user_id).one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized User')
    if not user.is_verified:
        raise HTTPException(status_code=401, detail='User is not verified')
    request.state.user = user
