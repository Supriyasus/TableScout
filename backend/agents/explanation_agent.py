from typing import Dict
from schemas.user_intent import UserIntent


class ExplanationAgent:
    """
    Generates human-readable explanations
    grounded in intent + place attributes.
    """

    def generate_explanation(self, place: Dict, intent: UserIntent) -> str:
        parts = []

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
            parts.append(
                f"it matches your preference for {', '.join(intent.descriptors[:2])}"
            )

        if not parts:
            return "This place matches your preferences."

        return "I recommended this place because " + ", ".join(parts) + "."
