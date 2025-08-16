# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:////Users/pllueca/Code/simple_social_network/social_network/core/repositories/sql/mydatabase.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    return session_maker()
