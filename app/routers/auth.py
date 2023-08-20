from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from sqlalchemy.orm import Session
from .. import database, schemas, models, utilis, oauth2


router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schemas.Token)
# def login(user_credintials: schemas.UserLogin, db: Session = Depends(database.get_db)):
def login(user_credintials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # OAuth2PasswordRequestForm this will prevent the user from adding the user credintials to be added in the body as json object
    # it should be passed through the form-data nd it will be like username => <email> password => <password >
    # OAuth2PasswordRequestForm this will return 2 things:
    # username =  (this is represents the email)
    # password =

    # user = db.query(models.User).filter(
    #     models.User.email == user_credintials.email).first()

    user = db.query(models.User).filter(
        models.User.email == user_credintials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credintials")

    if not utilis.verify(user_credintials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credintials")

    # create  token
    # return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer", }
