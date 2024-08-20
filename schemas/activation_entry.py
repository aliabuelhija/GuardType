from pydantic import BaseModel
import datetime


class FirstActivationRequest(BaseModel):
    username: str


class FirstActivationResponse(BaseModel):
    id: int
    username: str
    activation_time: datetime.datetime

    class Config:
        from_attributes = True
