from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/places", tags=["Places"])

class PlaceRequest(BaseModel):
    query: str               # natural language
    latitude: float
    longitude: float

@router.post("/recommend")
def recommend_places(request: PlaceRequest):
    return {"message": "Places API working"}
