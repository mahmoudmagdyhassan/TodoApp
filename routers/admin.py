from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path,Request
from starlette import status
from models import Todos,Users
from database import SessionLocal
from .auth import get_current_user
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="templates")
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


'''
@router.get("/users", response_class=HTMLResponse)
async def view_all_users(request: Request, user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Not authorized")
    
    users = db.query(Users).all()
    return templates.TemplateResponse("admin_users.html", {
        "request": request,
        "users": users,
        "user": user  # علشان تستخدمه في الـ navbar
    })

'''
# عرض كل المستخدمين
@router.get("/users", response_class=HTMLResponse)
async def view_all_users(request: Request, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authorized")
    
    # جلب كل المستخدمين من قاعدة البيانات
    users = db.query(Users).all()
    
    return templates.TemplateResponse("admin_users.html", {
        "request": request,
        "users": users,
        "user": user  # علشان تستخدمه في الـ navbar
    })








@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()