from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use SQLite for local testing
DATABASE_URL = "sqlite:///./railway.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()