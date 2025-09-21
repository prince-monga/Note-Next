#!/usr/bin/env python3
"""
Script to create demo data with Indian names
5 parents with 7 children total (3 parents have 1 child each, 2 parents have 2 children each)
"""
from database import SessionLocal, User, Folder, Note
from auth import get_password_hash
import random

def create_demo_data():
    db = SessionLocal()
    
    # Clear existing data
    db.query(Note).delete()
    db.query(Folder).delete()
    db.query(User).delete()
    db.commit()
    
    # Indian names for parents and children
    parent_names = [
        ("Rajesh", "rajesh.sharma@email.com"),
        ("Priya", "priya.patel@email.com"),
        ("Amit", "amit.kumar@email.com"),
        ("Sunita", "sunita.singh@email.com"),
        ("Vikram", "vikram.gupta@email.com")
    ]
    
    child_names = [
        ("Arjun", "arjun.sharma@email.com"),
        ("Kavya", "kavya.patel@email.com"),
        ("Rohan", "rohan.kumar@email.com"),
        ("Ananya", "ananya.kumar@email.com"),
        ("Ishaan", "ishaan.singh@email.com"),
        ("Diya", "diya.singh@email.com"),
        ("Aarav", "aarav.gupta@email.com")
    ]
    
    # Create parents
    parents = []
    for name, email in parent_names:
        parent = User(
            username=name.lower(),
            email=email,
            hashed_password=get_password_hash("password123"),
            role="parent"
        )
        db.add(parent)
        parents.append(parent)
    
    db.commit()
    db.refresh(parents[0])
    db.refresh(parents[1])
    db.refresh(parents[2])
    db.refresh(parents[3])
    db.refresh(parents[4])
    
    # Create children with parent assignments
    # First 3 parents get 1 child each, last 2 parents get 2 children each
    child_assignments = [0, 1, 2, 3, 3, 4, 4]  # Parent indices
    
    children = []
    for i, (name, email) in enumerate(child_names):
        parent_id = parents[child_assignments[i]].id
        child = User(
            username=name.lower(),
            email=email,
            hashed_password=get_password_hash("password123"),
            role="child",
            parent_id=parent_id
        )
        db.add(child)
        children.append(child)
    
    db.commit()
    
    # Refresh children to get their IDs
    for child in children:
        db.refresh(child)
    
    # Create folders for children
    folder_names = ["School", "Personal", "Projects", "Ideas", "To-Do"]
    folders = []
    
    for child in children:
        # Each child gets 2-3 random folders
        num_folders = random.randint(2, 3)
        child_folders = random.sample(folder_names, num_folders)
        
        for folder_name in child_folders:
            folder = Folder(
                name=folder_name,
                owner_id=child.id
            )
            db.add(folder)
            folders.append(folder)
    
    db.commit()
    
    # Refresh folders to get their IDs
    for folder in folders:
        db.refresh(folder)
    
    # Create notes for children
    note_templates = [
        ("Math Homework", "Complete algebra problems from chapter 5", "homework,math", True, False),
        ("Birthday Party Ideas", "Plan surprise party for mom's birthday", "family,celebration", False, False),
        ("Science Project", "Research on renewable energy sources", "school,science", True, False),
        ("Shopping List", "Buy groceries for the week", "shopping,groceries", True, True),
        ("Book Review", "Write review for 'The Alchemist'", "books,review", False, False),
        ("Weekend Plans", "Visit grandparents and go to park", "family,weekend", False, False),
        ("Study Schedule", "Prepare timetable for exams", "study,exams", True, False),
        ("Art Project", "Paint landscape for art class", "art,school", True, False),
        ("Friend's Contact", "Save new friend's phone number", "contacts,friends", False, False),
        ("Movie List", "Movies to watch during holidays", "entertainment,movies", False, False)
    ]
    
    for child in children:
        # Get child's folders
        child_folders = [f for f in folders if f.owner_id == child.id]
        
        # Each child gets 3-5 random notes
        num_notes = random.randint(3, 5)
        child_notes = random.sample(note_templates, num_notes)
        
        for title, content, tags, is_todo, is_completed in child_notes:
            # Randomly assign to folder or no folder
            if child_folders and random.choice([True, False]):
                folder_id = random.choice(child_folders).id
            else:
                folder_id = None
            
            note = Note(
                title=title,
                content=content,
                tags=tags,
                is_todo=is_todo,
                is_completed=is_completed,
                folder_id=folder_id,
                owner_id=child.id
            )
            db.add(note)
    
    db.commit()
    db.close()
    
    print("Demo data created successfully!")
    print("\nParents and their children:")
    print("1. rajesh (password: password123) - Child: arjun")
    print("2. priya (password: password123) - Child: kavya")
    print("3. amit (password: password123) - Child: rohan")
    print("4. sunita (password: password123) - Children: ananya, ishaan")
    print("5. vikram (password: password123) - Children: diya, aarav")
    print("\nAll children also have username/password combinations (password: password123)")

if __name__ == "__main__":
    create_demo_data()