from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import get_db, User, Folder, Note
from auth import get_password_hash, verify_password, create_access_token, get_current_user

app = FastAPI(title="NoteNext API")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "child"
    parent_id: Optional[int] = None
    child_ids: Optional[List[int]] = []

class UserLogin(BaseModel):
    username: str
    password: str

class FolderCreate(BaseModel):
    name: str

class NoteCreate(BaseModel):
    title: str
    content: str
    tags: Optional[str] = ""
    is_todo: bool = False
    folder_id: Optional[int] = None

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None
    is_todo: Optional[bool] = None
    is_completed: Optional[bool] = None

# Auth endpoints
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,
        parent_id=user.parent_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # If parent, link selected children
    if user.role == "parent" and user.child_ids:
        for child_id in user.child_ids:
            child = db.query(User).filter(User.id == child_id, User.role == "child").first()
            if child:
                child.parent_id = db_user.id
        db.commit()
    
    return {"message": "User created successfully"}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": db_user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "role": db_user.role
        }
    }

# Folder endpoints
@app.get("/folders")
def get_folders(child_id: Optional[int] = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role == "parent":
        # Parents can see their children's folders
        child_ids = [child.id for child in current_user.children]
        if child_id and child_id in child_ids:
            # Filter by specific child
            folders = db.query(Folder).filter(Folder.owner_id == child_id).all()
        else:
            # Show all children's folders
            folders = db.query(Folder).filter(Folder.owner_id.in_(child_ids)).all()
    else:
        # Children can only see their own folders
        folders = db.query(Folder).filter(Folder.owner_id == current_user.id).all()
    return folders

@app.post("/folders")
def create_folder(folder: FolderCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role == "parent":
        raise HTTPException(status_code=403, detail="Parents cannot create folders")
    
    db_folder = Folder(name=folder.name, owner_id=current_user.id)
    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)
    return db_folder

@app.delete("/folders/{folder_id}")
def delete_folder(folder_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    folder = db.query(Folder).filter(Folder.id == folder_id).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    if current_user.role == "parent" or folder.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(folder)
    db.commit()
    return {"message": "Folder deleted"}

# Note endpoints
@app.get("/notes")
def get_notes(folder_id: Optional[int] = None, child_id: Optional[int] = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(Note)
    
    if current_user.role == "parent":
        # Parents can see their children's notes
        child_ids = [child.id for child in current_user.children]
        if child_id and child_id in child_ids:
            # Filter by specific child
            query = query.filter(Note.owner_id == child_id)
        else:
            # Show all children's notes
            query = query.filter(Note.owner_id.in_(child_ids))
    else:
        # Children can only see their own notes
        query = query.filter(Note.owner_id == current_user.id)
    
    if folder_id:
        query = query.filter(Note.folder_id == folder_id)
    
    return query.all()

@app.post("/notes")
def create_note(note: NoteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role == "parent":
        raise HTTPException(status_code=403, detail="Parents cannot create notes")
    
    db_note = Note(
        title=note.title,
        content=note.content,
        tags=note.tags,
        is_todo=note.is_todo,
        folder_id=note.folder_id,
        owner_id=current_user.id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.put("/notes/{note_id}")
def update_note(note_id: int, note: NoteUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    if current_user.role == "parent" or db_note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    for field, value in note.dict(exclude_unset=True).items():
        setattr(db_note, field, value)
    
    db_note.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_note)
    return db_note

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if current_user.role == "parent" or note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}

@app.get("/children")
def get_children(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "parent":
        raise HTTPException(status_code=403, detail="Only parents can access this endpoint")
    
    children = [{
        "id": child.id,
        "username": child.username,
        "email": child.email
    } for child in current_user.children]
    return children

@app.get("/available-children")
def get_available_children(db: Session = Depends(get_db)):
    # Get children without parents
    children = db.query(User).filter(User.role == "child", User.parent_id == None).all()
    return [{
        "id": child.id,
        "username": child.username,
        "email": child.email
    } for child in children]

@app.get("/")
def root():
    return {"message": "NoteNext API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)