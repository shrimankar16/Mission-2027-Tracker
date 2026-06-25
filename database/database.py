"""
Database setup, connection management, and initialization
SQLite with WAL mode and foreign key enforcement
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool
import os
from pathlib import Path
from database.models import Base

# Database file path
DB_PATH = Path(__file__).parent.parent / "career_data.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create engine with SQLite optimizations
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30
    },
    poolclass=StaticPool,
    echo=False
)


# Enable WAL mode and foreign keys
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()


# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """Get a new database session"""
    return SessionLocal()


def init_database():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)


def is_database_empty():
    """Check if database is empty (no user profile)"""
    session = get_session()
    try:
        from database.models import UserProfile
        count = session.query(UserProfile).count()
        return count == 0
    except Exception:
        return True
    finally:
        session.close()


def backup_database():
    """Create a backup copy of the database"""
    from datetime import date
    from shutil import copy2
    
    if not DB_PATH.exists():
        return
    
    backup_dir = Path(__file__).parent.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    
    backup_file = backup_dir / f"career_db_{date.today().strftime('%Y%m%d')}.sqlite"
    
    try:
        copy2(DB_PATH, backup_file)
        print(f"Backup created: {backup_file}")
    except Exception as e:
        print(f"Backup failed: {e}")
