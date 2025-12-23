class PlaceRequest(BaseModel):
    mood: str
    budget: str
    time: str | None
    latitude: float
    longitude: float
