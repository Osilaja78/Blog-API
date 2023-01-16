from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter(prefix="/blog",tags=["Blog"])

@router.get("/", response_model=List[schemas.ShowBlog])
async def get_all_blog(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post("/", status_code=status.HTTP_201_CREATED)
async def blog(request: schemas.Blog, db: Session = Depends(get_db),
                current_user: schemas.User = Depends(get_current_user)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/{id}", response_model=schemas.ShowBlog)
async def get_specific_blog(id: int, response: Response, db: Session = Depends(get_db),
                            current_user: schemas.User = Depends(get_current_user)):

    blog_post = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Blog with id '{id}' not found!")

    return blog_post

@router.put("/{id}")
async def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db),
                        current_user: schemas.User = Depends(get_current_user)):
    blog_post = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog post with id '{id}' not found!")

    blog_post.update({'title': request.title, 'body': request.body})
    db.commit()
    return {
        'detail': 'Updated successfully'
    }

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db),
                        current_user: schemas.User = Depends(get_current_user)):
    blog_post = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)

    if not blog_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog post with id '{id}' not found!")
        
    db.commit()
    return {
        'detail': f'Blog post with id {id} deleted successfully!'
    }