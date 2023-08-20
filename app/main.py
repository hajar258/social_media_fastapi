from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from . import models, config
from .database import engine
from .routers import post, user, auth, vote
from pydantic_settings import BaseSettings

# this is the command that is used to tell sqlalchamy to generate all tables when we start the app or reload it, but we dont need it ny more as we are using alembic
# models.Base.metadata.create_all(bind=engine)

# fast Api instance
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # what domains can talk with our api!
    allow_credentials=True,
    # what http methods that you allow in your api exmple: only allow public people to send get requests not post, delete
    allow_methods=["*"],
    allow_headers=["*"],  # allow specific headers fro the request
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# this is a path operation >> it is just route!!
# this is decorator >>


@app.get("/")
# this is a function,
async def root():
    return {"message": "Welcome to my API!"}
