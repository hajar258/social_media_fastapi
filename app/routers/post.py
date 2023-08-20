
from .. import models, schemas, oauth2
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter

from ..database import get_db
from sqlalchemy.orm import Session

from sqlalchemy import func

from typing import Optional, List

router = APIRouter(
    prefix="/posts",  # this mean every route in this file will start with this prefix
    # this is used to put a group in the documentation to handel all routes related to posts
    tags=['Posts']

)


# if we pass only ==>  response_model=schemas.Post ==> this will give us an error as we are expecting list of posts not just one object ==> that is why we need to use List from typing library
@router.get("/", response_model=List[schemas.PostOut])
# limit variable is a query paramaeter that wi;; be passed to the request like that /posts?limit=2
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # to get all posts from db using SQL
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    # print(current_user.email)
    # to get all posts from db using sqlalchemy

    # this is to make user get his posts only!!!
    # posts = db.query(models.Post).filter(
    #     models.Post.owner_id == current_user.id).limit(limit).all()

    # this is to open all posts fro all users
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # this is to get the number of votes for each post
    post_vote = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(post_vote)
    # return {"data": posts}
    return post_vote

# @app.post("/createposts") -- this has been deleted as the name of the path is not as best practice -- it should be prular

# status_code=status.HTTP_201_CREATED adding this will change the default status code which was 200 with successfull request


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # insert a new post into db
    # using %s will secure us from sql injection
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #     [
    #         post.title, post.content, post.published
    #     ]
    # )
    # new_post = cursor.fetchone()

    # conn.commit()  # this is used to save changes to db, if we did not use it then the changes will not be saved to db, however in the api it will say that everything is working correctly.!! reall important

    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published)

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # retrieve the new row that is added

    # return {"data": new_post}
    return new_post


# id is called path parameter
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(type(id))
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, [id])
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    post_vote = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post_vote:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found!!")
    # return {"post_details": post}
    return post_vote


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # deletig post
    # find the index of the post in my_posts list
    # then delete it from the list
    # index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform the requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title=%s , content=%s, published=%s WHERE id=%s RETURNING *""",
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    query_post = db.query(models.Post).filter(models.Post.id == id)
    updated_post = query_post.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform the requested action")

    query_post.update(post.dict(), synchronize_session=False)
    db.commit()

    # return {'message': query_post.first()}
    return query_post.first()
