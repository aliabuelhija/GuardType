from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List
from db.models import OffensiveEntry, KeyboardChangeEntry
from schemas.statics import FrequentWordsSchema,ChangeRecord  , KeyboardUsageDailySchema, \
    HourlyOffensiveContentDetail, ChangeRecord
from db.database import get_db

router = APIRouter(
    prefix='/statics',
    tags=['statics']
)
def format_date(date_obj):
    return date_obj.strftime('%Y-%m-%d')
def calculate_daily_usage_for_day(db: Session, username: str, day_start: datetime, day_end: datetime):
    daily_usage = 0
    start_time = None

    entries = db.query(KeyboardChangeEntry)\
                .filter(KeyboardChangeEntry.username == username)\
                .filter(KeyboardChangeEntry.change_time >= day_start)\
                .filter(KeyboardChangeEntry.change_time < day_end)\
                .order_by(KeyboardChangeEntry.change_time)\
                .all()

    for entry in entries:
        if entry.new_keyboard == 'com.example.guardtype/.Services.GuardTypeService':
            start_time = entry.change_time
        elif entry.old_keyboard == 'com.example.guardtype/.Services.GuardTypeService' and start_time:
            end_time = entry.change_time
            daily_usage += (end_time - start_time).total_seconds() / 3600
            start_time = None

    if start_time:
        end_time = min(day_end, datetime.utcnow())
        daily_usage += (end_time - start_time).total_seconds() / 3600

    return day_start.date(), daily_usage

def calculate_daily_keyboard_usage(db: Session, username: str):
    current_time = datetime.utcnow()
    week_ago = current_time - timedelta(days=7)
    daily_usage = {}

    for day in range(8):
        day_start = week_ago + timedelta(days=day)
        day_end = day_start + timedelta(days=1)
        day_date, usage = calculate_daily_usage_for_day(db, username, day_start, day_end)
        daily_usage[day_date] = usage

    return daily_usage

def get_frequent_words(db: Session, username: str, current_time: datetime):
    week_ago = current_time - timedelta(days=7)
    words = db.query(OffensiveEntry.text, func.count(OffensiveEntry.text).label('count'))\
              .filter(OffensiveEntry.username == username)\
              .filter(OffensiveEntry.date >= week_ago)\
              .group_by(OffensiveEntry.text)\
              .order_by(func.count(OffensiveEntry.text).desc())\
              .limit(5)\
              .all()
    return words


def get_daily_keyboard_changes(db: Session, username: str, day_start: datetime, day_end: datetime):
    changes_count = db.query(func.count(KeyboardChangeEntry.id))\
                      .filter(KeyboardChangeEntry.username == username)\
                      .filter(KeyboardChangeEntry.change_time >= day_start)\
                      .filter(KeyboardChangeEntry.change_time < day_end)\
                      .filter(KeyboardChangeEntry.old_keyboard == 'com.example.guardtype/.Services.GuardTypeService')\
                      .filter(KeyboardChangeEntry.new_keyboard != 'com.example.guardtype/.Services.GuardTypeService')\
                      .scalar()
    return day_start.date().isoformat(), changes_count


def get_offensive_content_by_hour(db: Session, username: str, current_time: datetime):
    week_ago = current_time - timedelta(days=7)
    hourly_counts = {}

    entries = db.query(OffensiveEntry)\
                .filter(OffensiveEntry.username == username)\
                .filter(OffensiveEntry.date >= week_ago)\
                .all()

    # Initialize hourly counts for each hour of the day
    for hour in range(24):
        hourly_range = f"{hour}:00-{hour+1}:00"
        hourly_counts[hourly_range] = 0

    # Populate the counts for each entry
    for entry in entries:
        hour = entry.date.hour
        hourly_range = f"{hour}:00-{hour+1}:00"
        hourly_counts[hourly_range] += 1

    return hourly_counts






@router.get("/keyboard-usage-daily/{username}", response_model=List[KeyboardUsageDailySchema])
async def keyboard_usage_daily(username: str, db: Session = Depends(get_db)):
    daily_usage = calculate_daily_keyboard_usage(db, username)
    return [{"date": day, "usage_hours": hours} for day, hours in daily_usage.items()]

@router.get("/frequent-words/{username}", response_model=List[FrequentWordsSchema])
async def frequent_words_statistics(username: str, db: Session = Depends(get_db)):
    words = get_frequent_words(db, username, datetime.utcnow())
    return [{"word": word, "count": count} for word, count in words]


@router.get("/offensive-content-hours/{username}", response_model=List[HourlyOffensiveContentDetail])
async def offensive_content_hours(username: str, db: Session = Depends(get_db)):
    hourly_counts = get_offensive_content_by_hour(db, username, datetime.utcnow())
    return [{"time_range": time_range, "count": count} for time_range, count in hourly_counts.items()]







def get_daily_keyboard_changes(db: Session, username: str, day_start: datetime, day_end: datetime):
    changes_count = db.query(func.count(KeyboardChangeEntry.id))\
                      .filter(KeyboardChangeEntry.username == username)\
                      .filter(KeyboardChangeEntry.change_time >= day_start)\
                      .filter(KeyboardChangeEntry.change_time < day_end)\
                      .filter(KeyboardChangeEntry.old_keyboard.like('%guardtype%'))\
                      .filter(KeyboardChangeEntry.new_keyboard.notlike('%guardtype%'))\
                      .scalar()
    return day_start.date().isoformat(), changes_count

@router.get("/keyboard-changes/{username}", response_model=List[ChangeRecord])
async def keyboard_changes_statistics(username: str, db: Session = Depends(get_db)):
    current_time = datetime.utcnow()
    week_ago = current_time - timedelta(days=7)
    daily_changes = []

    for day in range(8):
        day_start = week_ago + timedelta(days=day)
        day_end = day_start + timedelta(days=1)
        day_date, changes_count = get_daily_keyboard_changes(db, username, day_start, day_end)
        daily_changes.append(ChangeRecord(date=day_date, changes_count=changes_count))

    if not daily_changes:
        raise HTTPException(status_code=404, detail="No data found")

    return daily_changes
