from pydantic import BaseModel
from typing import Optional
import datetime
from db.models import SourceEnum


class RecognizeWordEntryRequest(BaseModel):
    username: str
    text: str


class RecognizeWordEntryResponse(BaseModel):
    id: Optional[int] = None
    username: str
    text: str
    date: datetime.datetime
    source: SourceEnum

    class Config:
        from_attributes = True


class CheckSentenceRequest(BaseModel):
    username: str
    text: str


class CheckSentenceResponse(BaseModel):
    id: Optional[int] = None
    username: str
    text: str
    date: datetime.datetime
    source: Optional[SourceEnum] = None
    offensive: bool
