from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from sqlalchemy.orm import Session

from db.models import Users
from db.database import get_db
from schemas.user import LoginRequest, SignUpRequest, UserResponse

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Users).filter(request.username == Users.username, request.password == Users.password).first()
    if not user:
        raise HTTPException(status_code=401, detail='Invalid username or password')
    return {"message": "Login successful"}


@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(request.username == Users.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='Username already taken')

    new_user = Users(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user": {"username": new_user.username, "email": new_user.email}}


@router.get('/all', response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return users


@router.delete('/all/delete', status_code=status.HTTP_200_OK)
async def delete_all_users(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    for user in users:
        db.delete(user)
    db.commit()
    return {"message": "All users deleted successfully"}
