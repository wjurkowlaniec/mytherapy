from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from datetime import datetime, timedelta
import models
from models import User, Reminder, ReminderGroup, ReminderEntry, Schedule
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

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

@app.post("/users/", response_model=User)
def add_user(user: User, db: Session = Depends(get_db)):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users/{user_id}/reminders", response_model=List[Reminder])
def get_user_reminders(user_id: int, db: Session = Depends(get_db)):
    authenticate_user(user_id, db)
    now = datetime.now()
    end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59)

    reminders = db.query(Reminder).join(Schedule).filter(
        and_(Reminder.user_id == user_id, Schedule.recurrence.between(now, end_of_day))
    ).order_by(Schedule.recurrence).all()
    return reminders


@app.post("/users/{user_id}/reminders", response_model=Reminder)
def create_reminder(user_id: int, reminder: Reminder, db: Session = Depends(get_db)):
    authenticate_user(user_id, db)
    reminder.user_id = user_id
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


@app.post("/users/{user_id}/reminder_entries", response_model=ReminderEntry)
def complete_reminder(user_id: int, reminder_id: int, db: Session = Depends(get_db)):
    authenticate_user(user_id, db)
    reminder_entry = ReminderEntry(reminder_id=reminder_id, date_completed=datetime.utcnow())
    db.add(reminder_entry)
    db.commit()
    db.refresh(reminder_entry)
    return reminder_entry


@app.get("/users/{user_id}/reminder_groups", response_model=List[ReminderGroup])
def get_user_reminder_groups(user_id: int, db: Session = Depends(get_db)):
    authenticate_user(user_id, db)
    reminder_groups = db.query(ReminderGroup).filter(ReminderGroup.user_id == user_id).all()
    return reminder_groups


@app.post("/users/{user_id}/reminder_groups", response_model=ReminderGroup)
def create_reminder_group(user_id: int, reminder_group: ReminderGroup, db: Session = Depends(get_db)):
    authenticate_user(user_id, db)
    reminder_group.user_id = user_id
    db.add(reminder_group)
    db.commit()
    db.refresh(reminder_group)
    return reminder_group

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
