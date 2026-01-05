from typing import Dict
from schemas.user_intent import UserIntent


class PlannerAgent:
    """
    Converts structured intent into a search plan.
    """

    def create_plan(
        self,
        intent: UserIntent,
        latitude: float,
        longitude: float
    ) -> Dict:

        prefs = intent.preferences

        place_types = intent.place_types or ["restaurant", "cafe"]
        priorities = ["distance", "rating"]
        radius_km = 2.0
        booking_likely = intent.booking_required

        # Crowd sensitivity
        if prefs.get("crowd_quietness", 0) > 0.7:
            priorities.append("low_crowd")
            radius_km += 1.0

        # Food importance
        if prefs.get("food_quality", 0) > 0.7:
            priorities.append("rating")

        # Travel tolerance
        if prefs.get("travel_tolerance", 0) < 0.4:
            radius_km = min(radius_km, 2.0)

        return {
            "place_types": place_types,
            "radius_km": radius_km,
            "priorities": priorities,
            "booking_likely": booking_likely
        }
