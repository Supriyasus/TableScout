'''Given user input:
Mood, Budget, Time
It decides:
Place types, Search radius, Priority weights, Whether booking might be required'''
from typing import Dict, List, Optional
class PlannerAgent:
    """
    PlannerAgent converts user intent into a structured search plan.
    """

    def create_plan(
        self,
        mood: str,
        budget: str,
        time: Optional[str] = None
    ) -> Dict:
        """
        Creates a planning strategy based on user input.
        """

        mood = mood.lower()
        budget = budget.lower()

        place_types: List[str] = []
        priorities: List[str] = []
        radius_km: float = 2.0
        booking_likely: bool = False

        # ---- Mood-based planning ----
        if mood == "work":
            place_types = ["cafe", "coworking_space", "library"]
            priorities = ["quiet", "wifi", "distance"]
            radius_km = 2.0
            booking_likely = False

        elif mood == "date":
            place_types = ["restaurant", "cafe"]
            priorities = ["ambience", "rating", "distance"]
            radius_km = 3.0
            booking_likely = True

        elif mood == "quick bite":
            place_types = ["fast_food", "cafe"]
            priorities = ["speed", "distance", "price"]
            radius_km = 1.5
            booking_likely = False

        else:
            # Fallback
            place_types = ["restaurant", "cafe"]
            priorities = ["rating", "distance"]
            booking_likely = True

        # ---- Budget adjustment ----
        if budget == "low":
            priorities.append("price")
        elif budget == "high":
            priorities.append("rating")

        # ---- Time-based adjustment (optional) ----
        if time:
            priorities.append("open_now")

        return {
            "place_types": place_types,
            "radius_km": radius_km,
            "priorities": priorities,
            "booking_likely": booking_likely
        }
