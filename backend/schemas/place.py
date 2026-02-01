from pydantic import BaseModel
from typing import Optional, List

# 1. Keep your existing Request model
class PlaceRequest(BaseModel):
    mood: str
    budget: str
    time: Optional[str] = None
    latitude: float
    longitude: float

# 2. ADD THIS NEW RESPONSE MODEL
# This acts as the "Gatekeeper". If a field isn't listed here, 
# FastAPI deletes it before sending the JSON.
class PlaceResponse(BaseModel):
    id: str
    name: str
    address: Optional[str] = None
    
    # --- The Critical Fields for Booking ---
    website: Optional[str] = None
    phone: Optional[str] = None
    # ---------------------------------------

    latitude: float
    longitude: float
    distance: Optional[str] = None
    time: Optional[str] = None
    crowd: Optional[str] = "moderate"
    price: Optional[str] = "₹₹"
    categories: List[str] = []