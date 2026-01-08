from typing import Dict, List, Optional

from agents.intent_extraction_agent import IntentExtractionAgent
from agents.planner_agent import PlannerAgent
from agents.traffic_agent import TrafficAgent
from agents.popularity_agent import PopularityAgent
from agents.scoring_agent import ScoringAgent
from agents.explanation_agent import ExplanationAgent

from mcp_servers.maps_mcp import MapboxMCP

from sqlalchemy.orm import Session
from db.crud import get_user_preferences


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
        longitude: float,
        db: Session,
        user_id: Optional[str] = None
    ) -> Dict:
        """
        End-to-end recommendation pipeline (personalized)
        """

        # 1️⃣ Natural language → structured intent
        intent = self.intent_agent.extract(user_query)

        # 2️⃣ Load user preferences (NEW)
        user_preferences = None
        if user_id:
            pref_record = get_user_preferences(db, user_id)
            if pref_record:
                user_preferences = pref_record.preferences

        # 3️⃣ Planner decides search strategy (still intent-only)
        plan = self.planner.create_plan(
            intent=intent,
            latitude=latitude,
            longitude=longitude
        )

        all_places: List[Dict] = []

        # 4️⃣ Fetch places via Maps MCP
        for category in plan["place_types"]:
            places = self.maps.search_places(
                lat=latitude,
                lng=longitude,
                category=category,
                limit=10
            )
            all_places.extend(places)

        enriched_places: List[Dict] = []

        # 5️⃣ Enrich each place
        for place in all_places:

            # ---- Travel ----
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

        # 6️⃣ Score + rank (intent + preferences) ✅
        ranked_places = self.scoring.rank_places(
            enriched_places,
            intent=intent,
            user_preferences=user_preferences
        )

        # 7️⃣ Add explanations
        for place in ranked_places:
            place["explanation"] = self.explainer.generate_explanation(
                place=place,
                intent=intent,
                user_preferences=user_preferences
            )

        return {
            "intent": intent.model_dump(),
            "strategy_used": plan,
            "user_preferences_used": bool(user_preferences),
            "total_found": len(ranked_places),
            "results": ranked_places[:10]
        }
