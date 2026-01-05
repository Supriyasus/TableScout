class BookingRequest(BaseModel):
    place_id: str
    time: str
    people: int
    user_name: str
