from typing import Dict, List
from backend.schemas.user_intent import UserIntent


class ScoringAgent:
    """
    Scores places using intent-driven weights.
    """

    def score_place(self, place: Dict, intent: UserIntent) -> float:
        score = 0.0
        prefs = intent.preferences

        # Rating
        rating = place.get("rating")
        if rating:
            score += (rating / 5.0) * prefs.get("food_quality", 0.5) * 0.4

        # Travel
        travel_time = place.get("travel_time")
        if travel_time:
            travel_score = max(0, 1 - (travel_time / 30))
            score += travel_score * (1 - prefs.get("travel_tolerance", 0.5)) * 0.3

        # Crowd
        crowd = place.get("crowd_level")
        if crowd == "low":
            score += prefs.get("crowd_quietness", 0.5) * 0.2
        elif crowd == "medium":
            score += 0.1

        return round(min(score, 1.0), 2)

    def rank_places(
        self,
        places: List[Dict],
        intent: UserIntent
    ) -> List[Dict]:

        for place in places:
            place["final_score"] = self.score_place(place, intent)

        return sorted(places, key=lambda x: x["final_score"], reverse=True)
