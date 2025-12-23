from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/places", tags=["Places"])

class PlaceRequest(BaseModel):
    mood: str
    budget: str
    latitude: float
    longitude: float
    time: str | None = None

@router.post("/recommend")
def recommend_places(request: PlaceRequest):
    return {"message": "Places API working"}
