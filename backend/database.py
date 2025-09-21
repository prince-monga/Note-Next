from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# SQLite database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./notes_new.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="child")  # "child" or "parent"
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # For child users
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Self-referential relationship
    parent = relationship("User", remote_side=[id], back_populates="children")
    children = relationship("User", back_populates="parent")
    
    folders = relationship("Folder", back_populates="owner")
    notes = relationship("Note", back_populates="owner")

class Folder(Base):
    __tablename__ = "folders"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="folders")
    notes = relationship("Note", back_populates="folder")

class Note(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    tags = Column(String)  # Comma-separated tags
    is_todo = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    folder_id = Column(Integer, ForeignKey("folders.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner = relationship("User", back_populates="notes")
    folder = relationship("Folder", back_populates="notes")

# Create tables
Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()