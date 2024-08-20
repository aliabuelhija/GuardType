from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.orm import Session

from db.models import ActivationEntry, KeyboardChangeEntry, Users
from db.database import get_db
from typing import List

from schemas.activation_entry import FirstActivationResponse, FirstActivationRequest
from schemas.keyboard_change_entry import KeyboardChangeRequest, KeyboardChangeResponse
from services.notification_service import notify_first_active, notify_change

# Routers
activation_router = APIRouter(
    prefix='/activation',
    tags=['activation']
)

keyboard_router = APIRouter(
    prefix='/keyboard',
    tags=['keyboard']
)




@activation_router.post('/first_activation', response_model=FirstActivationResponse, status_code=status.HTTP_201_CREATED)
async def first_activation(request: FirstActivationRequest, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_entry = ActivationEntry(username=request.username)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    notify_first_active(user.email, user.username)

    new_keyboard_entry = KeyboardChangeEntry(
        username=request.username,
        old_keyboard="N/A",
        new_keyboard="com.example.guardtype/.Services.GuardTypeService",
    )
    db.add(new_keyboard_entry)
    db.commit()
    return new_entry


@activation_router.get('/all', response_model=List[FirstActivationResponse], status_code=status.HTTP_200_OK)
async def get_all_first_activations(db: Session = Depends(get_db)):
    activations = db.query(ActivationEntry).all()
    return activations


@activation_router.delete('/delete_all', status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_first_activations(db: Session = Depends(get_db)):
    db.query(ActivationEntry).delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@keyboard_router.post('/change', response_model=KeyboardChangeResponse, status_code=status.HTTP_201_CREATED)
async def keyboard_change(request: KeyboardChangeRequest, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_entry = KeyboardChangeEntry(username=request.username, old_keyboard=request.old_keyboard, new_keyboard=request.new_keyboard)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    notify_change(user.email, user.username, request.old_keyboard, request.new_keyboard)
    return new_entry


@keyboard_router.get('/all', response_model=List[KeyboardChangeResponse], status_code=status.HTTP_200_OK)
async def get_all_keyboard_changes( db: Session = Depends(get_db)):
    keyboard_changes = db.query(KeyboardChangeEntry).all()
    return keyboard_changes


@keyboard_router.delete('/delete_all', status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_keyboard_changes( db: Session = Depends(get_db)):
    db.query(KeyboardChangeEntry).delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
