from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.api.v1.deps import get_db, get_current_user
from backend.agents.orchestrator import OrchestratorAgent

router = APIRouter(prefix="/places", tags=["Places"])

class PlaceRequest(BaseModel):
    query: str               # natural language
    latitude: float
    longitude: float

# Initialize orchestrator once
orchestrator = OrchestratorAgent()

@router.post("/recommend")
def recommend_places(
    request: PlaceRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    Get personalized place recommendations for authenticated user
    """
    try:
        result = orchestrator.get_recommendations(
            user_query=request.query,
            latitude=request.latitude,
            longitude=request.longitude,
            db=db,
            user_id=current_user  # Use authenticated user
        )
        return result
    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to get recommendations"
        }
