import jwt

from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .. import CLIENT_SECRET
from ..database.models import User

SECRET_KEY = CLIENT_SECRET

oauth2_sch = OAuth2PasswordBearer(tokenUrl='/api/v1/auth')


def create_access_token(user, days=7):
    data = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(days=days)
    }
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def decode_access_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception as err:
        raise HTTPException(500, err)


def get_current_user(token: str = Depends(oauth2_sch)) -> User:
    data = decode_access_token(token)
    if data:
        return User.select().where(User.id == data['user_id']).first()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Access token not valid',
            headers={'WWW-Authenticate': 'Bearer'}
        )
