"""
CRUD operations for database models
"""
from sqlalchemy.orm import Session
from backend.db.models import User, UserPreference
from datetime import datetime

# -------------------------
# User (authentication)
# -------------------------

def get_user(db: Session, user_id: str):
    """
    Retrieve a user by ID
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user by email
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_id: str, email: str, hashed_password: str):
    """
    Create a new user record
    """
    user = User(
        id=user_id,
        email=email,
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# -------------------------
# UserPreference (personalization)
# -------------------------

def get_user_preferences(db: Session, user_id: str):
    """
    Retrieve user preferences by user_id
    """
    return db.query(UserPreference).filter(UserPreference.user_id == user_id).first()


def add_visited_place(db: Session, user_id: str, place_name: str):
    """
    Add a visited place to user preferences
    """
    record = get_user_preferences(db, user_id)
    if record:
        visited = record.preferences.get("visited_places", [])
        if place_name not in visited:
            visited.append(place_name)
            record.preferences["visited_places"] = visited
            record.last_updated = datetime.utcnow()
            db.commit()
            db.refresh(record)


def create_or_update_user_preference(db: Session, user_id: str, preferences: dict):
    """
    Create new user preference record or update existing one
    """
    record = get_user_preferences(db, user_id)
    if not record:
        record = UserPreference(
            user_id=user_id,
            preferences=preferences,
            last_updated=datetime.utcnow()
        )
        db.add(record)
    else:
        record.preferences = preferences
        record.last_updated = datetime.utcnow()
    db.commit()
    return record


def delete_user_preferences(db: Session, user_id: str):
    """
    Delete user preference record
    """
    record = get_user_preferences(db, user_id)
    if record:
        db.delete(record)
        db.commit()
    return record
