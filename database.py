from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///library.db", echo=True)
SessionLocal = sessionmaker(bind=engine)
db_session = SessionLocal()

Base = declarative_base()