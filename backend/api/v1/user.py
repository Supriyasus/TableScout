from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from backend.api.v1.deps import get_db, get_current_user
from backend.db.models import UserPreference

router = APIRouter(prefix="/user", tags=["User"])

class UserInteraction(BaseModel):
    signal: str
    place_type: str

@router.post("/interact")
def record_user_interaction(
    interaction: UserInteraction,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    Records user preference signals for authenticated user
    """

    record = (
        db.query(UserPreference)
        .filter(UserPreference.user_id == current_user)
        .first()
    )

    # Case 1: first time user
    if not record:
        record = UserPreference(
            user_id=current_user,
            preferences={
                "place_type_affinity": {
                    interaction.place_type: 1.0
                }
            },
            last_updated=datetime.utcnow()
        )
        db.add(record)

    # Case 2: returning user
    else:
        prefs = record.preferences
        affinity = prefs.get("place_type_affinity", {})

        affinity[interaction.place_type] = affinity.get(
            interaction.place_type, 0.0
        ) + 0.1   # simple increment (EMA later)

        prefs["place_type_affinity"] = affinity
        record.preferences = prefs
        record.last_updated = datetime.utcnow()

    db.commit()

    return {"status": "stored", "user_id": current_user}

@router.get("/preferences")
def get_user_preferences(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    Get preferences for authenticated user
    """
    record = (
        db.query(UserPreference)
        .filter(UserPreference.user_id == current_user)
        .first()
    )

    if not record:
        return {"user_id": current_user, "preferences": {}}

    return {
        "user_id": record.user_id,
        "preferences": record.preferences,
        "last_updated": record.last_updated
    }

