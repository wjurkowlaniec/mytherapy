from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.event import listen
from fixtures import populate_initial_data

DATABASE_URL = "sqlite:///./mytherapy.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Listen to the `after_create` event
listen(Base.metadata, 'after_create', populate_initial_data)
