from db_models import User, Schedule, ReminderGroup, Reminder


def populate_initial_data(session):
    # TODO not working yet
    # Create initial data
    user = User(name="John Doe")
    schedule = Schedule(recurrence="daily")
    reminder_group = ReminderGroup(name="Daily Tasks", user_id=user.id)
    reminder = Reminder(name="Take medication", user_id=user.id, schedule_id=schedule.id)

    # Add initial data to the session
    session.add(user)
    session.add(schedule)
    session.add(reminder_group)
    session.add(reminder)

    # Commit the transaction
    session.commit()
