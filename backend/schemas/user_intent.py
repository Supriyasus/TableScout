from pydantic import BaseModel
from typing import Dict, List, Optional


class UserIntent(BaseModel):
    descriptors: List[str]
    preferences: Dict[str, float]
    place_types: List[str]
    constraints: List[str]
    time_of_day: Optional[str] = None
    booking_required: bool = False
