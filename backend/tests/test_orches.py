# from app.mcp_servers.maps import MapboxMCP

# from ..agents.orchestrator import OrchestratorAgent
from agents.orchestrator import OrchestratorAgent
from api.v1.places import PlaceRequest

# from ..mcp_servers.maps_mcp import MapboxMCP

# mcp = MapboxMCP()



req = PlaceRequest(
    mood="hangout",
    budget="medium",
    latitude=28.6139,
    longitude=77.2090,
    time="evening"
)

orch = OrchestratorAgent()
print(orch.get_recommendations(req))
