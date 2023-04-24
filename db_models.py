from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reminders = relationship("Reminder", back_populates="user")
    reminder_groups = relationship("ReminderGroup", back_populates="user")


class Reminder(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    schedule_id = Column(Integer, ForeignKey('schedules.id'))
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="reminders")
    schedule = relationship("Schedule", back_populates="reminders")
    reminder_group_entries = relationship("ReminderGroupEntry", back_populates="reminder")
    reminder_entries = relationship("ReminderEntry", back_populates="reminder")


class ReminderGroup(Base):
    __tablename__ = 'reminder_groups'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="reminder_groups")
    reminder_group_entries = relationship("ReminderGroupEntry", back_populates="reminder_group")


class ReminderGroupEntry(Base):
    __tablename__ = 'reminder_group_entries'
    id = Column(Integer, primary_key=True)
    reminder_group_id = Column(Integer, ForeignKey('reminder_groups.id'), nullable=False)
    reminder_id = Column(Integer, ForeignKey('reminders.id'), nullable=False)
    order = Column(Integer, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reminder_group = relationship("ReminderGroup", back_populates="reminder_group_entries")
    reminder = relationship("Reminder", back_populates="reminder_group_entries")


class ReminderEntry(Base):
    __tablename__ = 'reminder_entries'
    id = Column(Integer, primary_key=True)
    reminder_id = Column(Integer, ForeignKey('reminders.id'), nullable=False)
    date_completed = Column(DateTime, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reminder = relationship("Reminder", back_populates="reminder_entries")


class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
    recurrence = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reminders = relationship("Reminder", back_populates="schedule")


engine = create_engine('sqlite:///reminders.db')
Base.metadata.create_all(engine)
