from typing import Dict, Optional, List
from backend.schemas.user_intent import UserIntent

class ExplanationAgent:
    """
    Generates human-readable explanations
    grounded in intent, place attributes, and user preferences.
    """

    def generate_explanation(
        self,
        place: Dict,
        intent: UserIntent,
        user_preferences: Optional[Dict] = None,
        visited_places: Optional[List[str]] = None
    ) -> str:
        parts = []

        # Unique place check
        if visited_places and place["name"] in visited_places:
            parts.append("you have already visited this place before")
        else:
            parts.append("this is a new place you haven't been to yet")

        # Travel time
        travel_time = place.get("travel_time")
        if travel_time is not None:
            parts.append(f"it is about {travel_time} minutes away considering traffic")

        # Crowd
        crowd = place.get("crowd_level")
        category = place.get("category", "").lower()

        if crowd == "low":
            if category == "bar":
                parts.append("it has a relaxed vibe right now")
            elif category == "cafe":
                parts.append("it’s peaceful and not too busy")
            elif category == "restaurant":
                parts.append("it’s calm and easy to get a table")
            elif category == "lounge":
                parts.append("it’s quiet and perfect for unwinding")
            elif category == "bakery":
                parts.append("it’s cozy with only a few customers")
            else:
                parts.append("it’s quiet at this time")

        elif crowd == "medium":
            if category == "bar":
                parts.append("it has a good buzz without being overwhelming")
            elif category == "cafe":
                parts.append("it has a steady flow of visitors")
            elif category == "restaurant":
                parts.append("it’s moderately busy, but tables are available")
            elif category == "lounge":
                parts.append("it has a balanced atmosphere with some groups around")
            elif category == "bakery":
                parts.append("it’s pleasantly active with regular customers")
            else:
                parts.append("it has a moderate crowd level")

        elif crowd == "high":
            if category == "bar":
                parts.append("it’s lively and packed right now")
            elif category == "cafe":
                parts.append("it’s bustling with people enjoying coffee")
            elif category == "restaurant":
                parts.append("it’s busy and may require a wait")
            elif category == "lounge":
                parts.append("it’s buzzing with activity and groups")
            elif category == "bakery":
                parts.append("it’s crowded with customers picking up fresh items")
            else:
                parts.append("it can be crowded right now")


        # Preference alignment
        if intent.descriptors:
            parts.append(f"it matches your preference for {', '.join(intent.descriptors[:2])}")

        if user_preferences and "place_type_affinity" in user_preferences:
            affinity = user_preferences["place_type_affinity"].get(place.get("category"))
            if affinity:
                parts.append(f"your affinity for {place['category']} boosted this recommendation")

        return "I recommended this place because " + ", ".join(parts) + "."
