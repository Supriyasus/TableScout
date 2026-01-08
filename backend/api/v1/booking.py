from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/booking", tags=["Booking"])

class BookingRequest(BaseModel):
    place_id: str
    time: str
    people: int
    user_name: str
    confirm: bool

@router.post("/create")
def create_booking(request: BookingRequest):
    return {
        "status": "pending",
        "message": "Booking request received. Booking MCP will be added soon."
    }
