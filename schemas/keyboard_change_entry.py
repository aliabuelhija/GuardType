from pydantic import BaseModel
import datetime


class KeyboardChangeRequest(BaseModel):
    username: str
    old_keyboard: str
    new_keyboard: str


class KeyboardChangeResponse(BaseModel):
    id: int
    username: str
    old_keyboard: str
    new_keyboard: str
    change_time: datetime.datetime

    class Config:
        from_attributes = True
