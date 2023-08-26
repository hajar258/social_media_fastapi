from jose import JWTError, jwt
from datetime import datetime,  timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from . import schemas, database, models
from sqlalchemy.orm import Session

from .config import settings

# this is the endpoint of the user authentication, login path
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# Algorithm
# Expiration date

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes  # 10 mins to expire


def create_access_token(data: dict):
    # thi is to create a copy of our data that is passed through the request in or out!
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # this is to create the jwt token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
        return token_data
    except JWTError:
        raise credentials_exception


# take the token from the request automtically, verify if the token is correct or not using "verify_access_token" method, extract the id for us, then we can automatically fetch the user from database and then add as parmeter

#
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credintials", headers={"WWW-Authenticte": "Bearer"})

    # here we can retrieve the data of the current user from db
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
