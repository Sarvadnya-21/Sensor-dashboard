import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use SQLite for easy local run (no MySQL required). Set USE_SQLITE=0 to use MySQL.
USE_SQLITE = os.getenv("USE_SQLITE", "1").lower() in ("1", "true", "yes")

Base = declarative_base()

def get_db_engine():
    if USE_SQLITE:
        db_path = os.path.join(os.path.dirname(__file__), "..", "sensor_data.db")
        url = f"sqlite:///{os.path.abspath(db_path)}"
        print(f"Using SQLite: {db_path}")
        return create_engine(url, connect_args={"check_same_thread": False})

    # MySQL configuration
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "sensor_dashboard")
    ROOT_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
    DATABASE_URL = f"{ROOT_URL}/{DB_NAME}"

    try:
        root_engine = create_engine(ROOT_URL)
        with root_engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"))
        print(f"Database '{DB_NAME}' ensured.")
    except OperationalError as e:
        print(f"Warning: Could not connect to MySQL. Error: {e}")

    return create_engine(DATABASE_URL, pool_pre_ping=True)

engine = get_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
