from typing import List, Optional, Any, Dict
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.api.v1.deps import get_db, get_current_user
from backend.agents.orchestrator import OrchestratorAgent

router = APIRouter(prefix="/places", tags=["Places"])

# --- SCHEMAS ---

class PlaceRequest(BaseModel):
    query: str
    latitude: float
    longitude: float

class PlaceResponse(BaseModel):
    place_id: str
    name: str
    address: Optional[str] = None
    latitude: float
    longitude: float
    categories: List[str] = []
    
    # Critical fields for Booking Button
    website: Optional[str] = None
    phone: Optional[str] = None

    # --- FIX: Add these so Pydantic doesn't filter them out ---
    distance_km: Optional[float] = None
    travel_time: Optional[int] = None
    # ----------------------------------------------------------

    # Legacy fields (keep them if you want, but the above two are what Orchestrator sends)
    distance: Optional[str] = None
    time: Optional[str] = None
    crowd: Optional[str] = "moderate"
    price: Optional[str] = "₹₹"
    explanation: Optional[str] = None 

orchestrator = OrchestratorAgent()

@router.post("/recommend", response_model=List[PlaceResponse])
def recommend_places(
    request: PlaceRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    try:
        orchestrator_output = orchestrator.get_recommendations(
            user_query=request.query,
            latitude=request.latitude,
            longitude=request.longitude,
            db=db,
            user_id=current_user
        )
        
        # Extract list logic
        if isinstance(orchestrator_output, dict):
            return orchestrator_output.get("results", [])
            
        return orchestrator_output
        
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return []