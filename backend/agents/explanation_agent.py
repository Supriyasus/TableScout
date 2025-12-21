'''For each recommended place:
Mention distance (traffic-aware)
Mention rating
Mention crowd/popularity
Mention budget/mood match
Produce short, friendly explanation'''

from typing import Dict
class ExplanationAgent:
    """
    ExplanationAgent generates human-readable explanations
    for why a place was recommended.
    """

    def generate_explanation(self, place: Dict) -> str:
        """
        Creates a concise explanation based on place attributes.
        """

        parts = []

        # Distance / travel time
        travel_time = place.get("travel_time")
        if travel_time:
            parts.append(
                f"it is about {travel_time} minutes away considering current traffic"
            )

        # Rating
        rating = place.get("rating")
        if rating:
            parts.append(f"it has a rating of {rating}")

        # Crowd level
        crowd = place.get("crowd_level")
        if crowd:
            if crowd == "low":
                parts.append("it is usually quiet at this time")
            elif crowd == "medium":
                parts.append("it has a moderate crowd level")
            elif crowd == "high":
                parts.append("it can be a bit crowded right now")

        # Budget match
        if place.get("budget_match"):
            parts.append("it fits your budget")

        # Mood match
        mood = place.get("mood_match")
        if mood:
            parts.append(f"it suits your {mood} preference")

        # Fallback
        if not parts:
            return "This place matches your preferences."

        explanation = "I recommended this place because " + ", ".join(parts) + "."

        return explanation
