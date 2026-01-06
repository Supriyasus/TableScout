from agents.orchestrator import OrchestratorAgent
from api.v1.places import PlaceRequest

orchestrator = OrchestratorAgent()

req = PlaceRequest(
    query="I want a calm cozy place to hang out with good food",
    latitude=28.6139,
    longitude=77.2090
)

result = orchestrator.get_recommendations(
    user_query=req.query,
    latitude=req.latitude,
    longitude=req.longitude
)

print(result)
