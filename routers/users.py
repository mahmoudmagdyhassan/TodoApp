from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path,Request
from starlette import status
from models import Users
from database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
'''
router = APIRouter(
    prefix='/user',
    tags=['user']
)
'''
router = APIRouter(prefix="/users", tags=["user"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
templates = Jinja2Templates(directory="templates")


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get('/profile', status_code=status.HTTP_200_OK)
async def get_user(request: Request, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_data = db.query(Users).filter(Users.id == user.get("id")).first()
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Use Jinja2Templates to render the profile page with user data
    return templates.TemplateResponse("profile.html", {"request": request, "user": user_data})



from pydantic import BaseModel

class UserVerification(BaseModel):
    password: str
    new_password: str

from fastapi import Form

@router.post("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, 
    db: db_dependency,
    password: str = Form(...),
    new_password: str = Form(...)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    # تحقق من الباسورد القديم
    if not bcrypt_context.verify(password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password change")

    # تحديث الباسورد الجديد
    user_model.hashed_password = bcrypt_context.hash(new_password)
    db.add(user_model)
    db.commit()
    print("password change")








@router.post("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phonenumber(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
    print("mobile change")
