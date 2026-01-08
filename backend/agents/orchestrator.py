from typing import Dict, List

from backend.agents.intent_extraction_agent import IntentExtractionAgent
from backend.mcp_servers.maps_mcp import MapboxMCP

from backend.agents.planner_agent import PlannerAgent
from backend.agents.traffic_agent import TrafficAgent
from backend.agents.popularity_agent import PopularityAgent
from backend.agents.scoring_agent import ScoringAgent
from backend.agents.explanation_agent import ExplanationAgent


class OrchestratorAgent:
    """
    OrchestratorAgent coordinates all agents and MCPs
    to produce final recommendations.
    """

    def __init__(self):
        self.intent_agent = IntentExtractionAgent()
        self.maps = MapboxMCP()

        self.planner = PlannerAgent()
        self.traffic = TrafficAgent()
        self.popularity = PopularityAgent()
        self.scoring = ScoringAgent()
        self.explainer = ExplanationAgent()

    def get_recommendations(
        self,
        user_query: str,
        latitude: float,
        longitude: float
    ) -> Dict:
        """
        End-to-end recommendation pipeline
        """

        # 1️⃣ Natural language → structured intent
        intent = self.intent_agent.extract(user_query)

        # 2️⃣ Planner decides search strategy
        plan = self.planner.create_plan(
            intent=intent,
            latitude=latitude,
            longitude=longitude
        )

        all_places: List[Dict] = []

        # 3️⃣ Fetch places via Maps MCP
        for category in plan["place_types"]:
            places = self.maps.search_places(
                lat=latitude,
                lng=longitude,
                category=category,
                limit=10
            )
            all_places.extend(places)

        enriched_places: List[Dict] = []

        # 4️⃣ Enrich each place
        for place in all_places:

            # ---- Travel (raw) ----
            travel = self.maps.get_travel_time(
                origin_lat=latitude,
                origin_lng=longitude,
                dest_lat=place["latitude"],
                dest_lng=place["longitude"]
            )

            place["distance_km"] = travel["distance_km"]
            place["travel_time"] = travel["travel_time"]

            # ---- Traffic normalization ----
            traffic = self.traffic.analyze_traffic(place)
            place.update(traffic)

            # ---- Popularity ----
            pop = self.popularity.estimate_crowd(
                place=place,
                time_of_day=intent.time_of_day
            )

            place["crowd_level"] = pop["crowd_level"]
            place["crowd_confidence"] = pop["confidence"]

            enriched_places.append(place)

        # 5️⃣ Score + rank (intent-aware)
        ranked_places = self.scoring.rank_places(
            enriched_places,
            intent=intent
        )

        # 6️⃣ Add explanations
        for place in ranked_places:
            place["explanation"] = self.explainer.generate_explanation(
                place=place,
                intent=intent
            )

        return {
            "intent": intent.model_dump(),
            "strategy_used": plan,
            "total_found": len(ranked_places),
            "results": ranked_places[:10]
        }
