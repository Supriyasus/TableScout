from fastapi import APIRouter
from pydantic import BaseModel
# from backend.agents.orchestrator_agent import OrchestratorAgent
from backend.agents.orchestrator import OrchestratorAgent

router = APIRouter(prefix="/places", tags=["Places"])

orchestrator = OrchestratorAgent()
class PlaceRequest(BaseModel):
    query: str
    latitude: float
    longitude: float

@router.post("/recommend")
def recommend_places(request: PlaceRequest):
    response = orchestrator.get_recommendations(
        user_query=request.query,
        latitude=request.latitude,
        longitude=request.longitude
    )
    return response
