from sqlalchemy import Column, String, Integer, DateTime, Enum
from .database import Base
import datetime
from enum import Enum as PyEnum
class Users(Base):
    __tablename__ = 'users'

    username = Column(String(50), primary_key=True, unique=True, index=True)
    email = Column(String(100))
    password = Column(String(100))



class SourceEnum(PyEnum):
    SERVER = "server"
    ROOM_SQL = "room_sql"

class OffensiveEntry(Base):
    __tablename__ = 'offensive_entries'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True)
    text = Column(String(1000))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    source = Column(Enum(SourceEnum), default=SourceEnum.SERVER)


class ActivationEntry(Base):
    __tablename__ = 'activation_entries'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True)
    activation_time = Column(DateTime, default=datetime.datetime.utcnow)

class KeyboardChangeEntry(Base):
    __tablename__ = 'keyboard_change_entries'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True)
    old_keyboard = Column(String(100))
    new_keyboard = Column(String(100))
    change_time = Column(DateTime, default=datetime.datetime.utcnow)
