from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List
from backend.api.v1.deps import get_current_user

router = APIRouter(prefix="/booking", tags=["Booking"])

# Simulated in-memory booking store
bookings = []

class BookingRequest(BaseModel):
    place_id: str
    time: datetime

class BookingResponse(BaseModel):
    message: str
    booking_id: int

@router.post("/", response_model=BookingResponse)
def create_booking(
    request: BookingRequest,
    user_id: str = Depends(get_current_user)
):
    booking_id = len(bookings) + 1
    booking = {
        "id": booking_id,
        "user_id": user_id,
        "place_id": request.place_id,
        "time": request.time.isoformat(),
        "status": "confirmed"
    }
    bookings.append(booking)
    return {"message": "Booking confirmed", "booking_id": booking_id}
