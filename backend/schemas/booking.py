from pydantic import BaseModel
from typing import Optional

class BookingRequest(BaseModel):
    place_id: str
    place_name: str               # Essential: Logs the name of the cafe
    time: str
    booking_url: Optional[str] = None  # Essential: Logs the link used
    
    # You can keep these if your logic uses them, 
    # but 'user_id' usually comes from the token, not the request body.
    people: int = 2
    user_name: Optional[str] = None

class BookingResponse(BaseModel):
    message: str
    booking_id: int
    external_url: Optional[str] = None