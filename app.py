from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import and_
from typing import List
from datetime import datetime, timedelta
import db_models
from db_models import User, Reminder, ReminderGroup, ReminderEntry, Schedule
from database import SessionLocal, engine

from models import UserCreate, UserOut, ReminderCreate, ReminderOut, ReminderGroupCreate, ReminderGroupOut, ReminderEntryCreate, ReminderEntryOut, ScheduleCreate, ScheduleOut

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=UserOut)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




@app.get("/users/{user_id}/reminders", response_model=List[ReminderOut])
def get_user_reminders(user_id: int, db: Session = Depends(get_db)):
    authenticate_user(user_id, db)
    now = datetime.now()
    end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59)

    reminders = db.query(Reminder).join(Schedule).filter(
        and_(Reminder.user_id == user_id, Schedule.recurrence.between(now, end_of_day))
    ).order_by(Schedule.recurrence).all()
    return reminders

@app.post("/users/{user_id}/reminders", response_model=ReminderOut)
def create_reminder(user_id: int, reminder: ReminderCreate, db: Session = Depends(get_db)):
    authenticate_user(user_id, db)
    db_reminder = Reminder(**reminder.dict(), user_id=user_id)
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

@app.post("/users/{user_id}/reminder_entries", response_model=ReminderEntryOut)
def complete_reminder(user_id: int, reminder_id: int, db: Session = Depends(get_db)):
    authenticate_user(user_id, db)
    reminder_entry = ReminderEntry(reminder_id=reminder_id, date_completed=datetime.utcnow())
    db.add(reminder_entry)
    db.commit()
    db.refresh(reminder_entry)
    return reminder_entry


@app.get("/users/{user_id}/reminder_groups", response_model=List[ReminderGroupOut])
def get_user_reminder_groups(user_id: int, db: Session = Depends(get_db)):
    authenticate_user(user_id, db)
    reminder_groups = db.query(ReminderGroup).filter(ReminderGroup.user_id == user_id).all()
    return reminder_groups

@app.post("/users/{user_id}/reminder_groups", response_model=ReminderGroupOut)
def create_reminder_group(user_id: int, reminder_group: ReminderGroupCreate, db: Session = Depends(get_db)):
    authenticate_user(user_id, db)
    db_reminder_group = ReminderGroup(name=reminder_group.name, user_id=user_id)
    db.add(db_reminder_group)
    db.flush()

    for reminder_id in reminder_group.reminder_ids:
        db.add(ReminderGroupEntry(reminder_group_id=db_reminder_group.id, reminder_id=reminder_id))

    db.commit()
    db.refresh(db_reminder_group)
    return db_reminder_group

@app.delete("/users/{user_id}/reminder_groups/{reminder_group_id}")
def delete_reminder_group(user_id: int, reminder_group_id: int, db: Session = Depends(get_db)):
    authenticate_user(user_id, db)
    reminder_group = db.query(ReminderGroup).filter(
        ReminderGroup.id == reminder_group_id, ReminderGroup.user_id == user_id
    ).first()

    if not reminder_group:
        raise HTTPException(status_code=404, detail="Reminder group not found")

    db.delete(reminder_group)
    db.commit()


@app.delete("/users/{user_id}/reminders/{reminder_id}")
def delete_reminder(user_id: int, reminder_id: int, db: Session = Depends(get_db)):
    authenticate_user(user_id, db)
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id, Reminder.user_id == user_id
    ).first()

    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")

    db.delete(reminder)
    db.commit()

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = authenticate_user(user_id, db)
    db.delete(user)
    db.commit()



@app.post("/schedules/", response_model=ScheduleOut)
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = Schedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@app.delete("/schedules/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()

    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    db.delete(schedule)
    db.commit()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Update this to the correct frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
