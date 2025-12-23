from typing import List, Dict


from ..mcp_servers.maps_mcp import MapboxMCP
from ..agents.planner_agent import PlannerAgent
from ..agents.traffic_agent import TrafficAgent
from ..agents.popularity_agent import PopularityAgent
from ..agents.scoring_agent import ScoringAgent
from ..agents.explanation_agent import ExplanationAgent


class OrchestratorAgent:

    def __init__(self):
        self.maps = MapboxMCP()
        self.planner = PlannerAgent()
        self.traffic = TrafficAgent()
        self.popularity = PopularityAgent()
        self.scoring = ScoringAgent()
        self.explainer = ExplanationAgent()

    def get_recommendations(self, request) -> Dict:
        """
        Main AI pipeline controller
        """

        # 1️⃣ Planner decides search strategy
        plan = self.planner.create_plan(
            mood=request.mood,
            budget=request.budget,
            time=request.time
        )
        categories = plan["place_types"]
        radius = plan["radius_km"]

        lat = request.latitude
        lng = request.longitude

        all_places = []

        # 2️⃣ Fetch places for each category
        for category in categories:
            places = self.maps.search_places(
                lat=lat,
                lng=lng,
                category=category,
                limit=10
            )
            all_places.extend(places)

        enriched_places = []

        # 3️⃣ Enrich each result
        for place in all_places:

            travel = self.maps.get_travel_time(
                origin_lat=lat,
                origin_lng=lng,
                dest_lat=place["latitude"],
                dest_lng=place["longitude"]
            )

            popularity_score = self.popularity.estimate_crowd(
                place=place,
                time_of_day=request.time
            )

            enriched_places.append({
                **place,
                "distance_km": travel["distance_km"],
                "travel_time_min": travel["travel_time"],
                "popularity_score": popularity_score
            })

        # 4️⃣ Score + Rank
        ranked = self.scoring.rank_places(enriched_places)

        # 5️⃣ Add Explanation
        explained = []
        for p in ranked:
            p["explanation"] = self.explainer.explain_choice(p)
            explained.append(p)

        return {
            "results": explained[:10],   # top 10
            "total_found": len(explained),
            "strategy_used": plan
        }
