from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time 

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please set it in your .env file or Docker Compose.")

engine = None
max_retries = 10
retry_delay_seconds = 5

for i in range(max_retries):
    try:
        temp_engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
        )
        with temp_engine.connect() as connection:
            print(f"Database connection successful on attempt {i+1}!")
            engine = temp_engine 
            break
    except Exception as e:
        print(f"Database connection attempt {i+1} failed: {e}")
        if i < max_retries - 1:
            print(f"Retrying in {retry_delay_seconds} seconds...")
            time.sleep(retry_delay_seconds)
        else:
            print("Max database connection retries exceeded.")
            raise

if engine is None:
    raise Exception("Failed to establish database connection after multiple retries.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """FastAPI dependency for database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()