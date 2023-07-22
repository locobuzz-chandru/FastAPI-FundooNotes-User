from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from core.database import get_db
from core.utils import Hasher, JWT
from logger import logger
from .models import User
from .tasks import send_email
from .validators import UserValidator, UserLogin

user_router = APIRouter()


@user_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserValidator, response: Response, db: Session = Depends(get_db)):
    try:
        user_dict = user.model_dump()
        user_dict.update({"password": Hasher.get_password_hash(user.password)})
        user_obj = User(**user_dict)
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        token = JWT.jwt_encode({"user": user_obj.id})
        send_email.delay(email=user_obj.email, token=token)
        return {"message": "Registered", "status": 201, "token": token}
    except Exception as e:
        logger.exception(e.args[0])
        response.status_code = 400
        return {'message': e.args[0], 'status': 400, 'data': {}}


@user_router.get("/verify_token/{token}")
def verify_token(token: str, response: Response, db: Session = Depends(get_db)):
    try:
        payload = JWT.jwt_decode(token)
        user_obj = db.query(User).filter_by(id=payload.get("user")).one_or_none()
        if not user_obj:
            raise Exception('User not found')
        user_obj.is_verified = True
        db.commit()
        db.refresh(user_obj)
        return {"message": "Token is verified", "status": 200, "data": {}}
    except Exception as e:
        logger.exception(e.args[0])
        response.status_code = 400
        return {'message': e.args[0], 'status': 400, 'data': {}}


@user_router.post('/login', status_code=status.HTTP_200_OK)
def login(response: Response, user: UserLogin, db: Session = Depends(get_db)):
    try:
        user_obj = db.query(User).filter_by(username=user.username).first()
        if user_obj and Hasher.verify_password(user.password, user_obj.password):
            token = JWT.jwt_encode({'user': user_obj.id})
            return {"message": 'Logged in successfully', 'status': 200, 'access_token': token}
        response.status_code = status.HTTP_401_UNAUTHORIZED
        raise Exception("Invalid credentials")
    except Exception as e:
        logger.exception(e.args[0])
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': e.args[0], 'status': 400, 'data': {}}


@user_router.get('/authenticate_user', status_code=status.HTTP_200_OK)
def authenticate_user(response: Response, token: str, db: Session = Depends(get_db)):
    try:
        payload = JWT.jwt_decode(token=token)
        user = db.query(User).filter_by(id=payload.get('user')).one_or_none()
        return user.id
    except Exception as e:
        logger.exception(e.args[0])
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'message': e.args[0], 'status': 401, 'data': {}}


@user_router.get('/retrieve_user/', status_code=status.HTTP_200_OK)
def retrieve_user(response: Response, user: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter_by(id=user).one_or_none()
        return user.id
    except Exception as e:
        logger.exception(e.args[0])
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': e.args[0], 'status': 400, 'data': {}}
