from pydantic import BaseModel
from datetime import date
class KeyboardUsageDailySchema(BaseModel):
    date: date
    usage_hours: float

class FrequentWordsSchema(BaseModel):
    word: str
    count: int

class WeeklyChangesSchema(BaseModel):
    changes_count: int


class HourlyOffensiveContentDetail(BaseModel):
    time_range: str
    count: int


class ChangeRecord(BaseModel):
    date: str
    changes_count: int

