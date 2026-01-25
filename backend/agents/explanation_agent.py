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

        # Rating
        rating = place.get("rating")
        if rating:
            parts.append(f"it has a rating of {rating}")

        # Crowd
        crowd = place.get("crowd_level")
        if crowd == "low":
            parts.append("it is usually quiet at this time")
        elif crowd == "medium":
            parts.append("it has a moderate crowd level")
        elif crowd == "high":
            parts.append("it can be crowded right now")

        # Preference alignment
        if intent.descriptors:
            parts.append(f"it matches your preference for {', '.join(intent.descriptors[:2])}")

        if user_preferences and "place_type_affinity" in user_preferences:
            affinity = user_preferences["place_type_affinity"].get(place.get("category"))
            if affinity:
                parts.append(f"your affinity for {place['category']} boosted this recommendation")

        return "I recommended this place because " + ", ".join(parts) + "."
