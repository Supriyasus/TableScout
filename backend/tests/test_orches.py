from backend.agents.orchestrator import OrchestratorAgent
from backend.api.v1.places import PlaceRequest
from backend.db.session import SessionLocal

orchestrator = OrchestratorAgent()

req = PlaceRequest(
    query="I want a calm cozy place to hang out with good food",
    latitude=28.6139,
    longitude=77.2090
)
db = SessionLocal()
result = orchestrator.get_recommendations(
    db=db,
    user_query=req.query,
    latitude=req.latitude,
    longitude=req.longitude
)

print(result)
