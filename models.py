from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from datetime import datetime, timedelta
import db_models
from db_models import User, Reminder, ReminderGroup, ReminderEntry, Schedule
from database import SessionLocal, engine

db_models.Base.metadata.create_all(bind=engine)

# Pydantic models
class UserCreate(BaseModel):
    name: str

class UserOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ReminderCreate(BaseModel):
    name: str
    schedule_id: int

class ReminderOut(BaseModel):
    id: int
    user_id: int
    name: str
    schedule_id: int

    class Config:
        orm_mode = True

class ReminderGroupCreate(BaseModel):
    name: str

class ReminderGroupOut(BaseModel):
    id: int
    user_id: int
    name: str

    class Config:
        orm_mode = True

class ReminderEntryCreate(BaseModel):
    reminder_id: int

class ReminderEntryOut(BaseModel):
    id: int
    reminder_id: int
    date_completed: datetime

    class Config:
        orm_mode = True


class ScheduleCreate(BaseModel):
    recurrence: str

class ScheduleOut(BaseModel):
    id: int
    recurrence: str

    class Config:
        orm_mode = True

class ReminderGroupCreate(BaseModel):
    name: str
    reminder_ids: List[int]

