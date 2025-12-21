# This agent takes enriched places (distance, traffic, crowd, rating, budget match, mood match) and computes a final score so places can be ranked.
# app/agents/scoring_agent.py

from typing import Dict, List


class ScoringAgent:
    """
    ScoringAgent computes a final score for each place
    using multiple normalized factors.
    """

    def score_place(self, place: Dict) -> float:
        """
        Computes a score between 0 and 1 for a single place.
        """

        score = 0.0

        # ---- Rating (0–5 → 0–1) ----
        rating = place.get("rating")
        if rating is not None:
            score += (rating / 5.0) * 0.30

        # ---- Travel time (lower is better) ----
        travel_time = place.get("travel_time")  # minutes
        if travel_time is not None:
            # assume 30 min is worst acceptable
            travel_score = max(0, 1 - (travel_time / 30))
            score += travel_score * 0.30

        # ---- Crowd level ----
        crowd = place.get("crowd_level")
        if crowd == "low":
            score += 0.15
        elif crowd == "medium":
            score += 0.08
        elif crowd == "high":
            score += 0.02

        # ---- Budget match ----
        if place.get("budget_match"):
            score += 0.15

        # ---- Mood match ----
        if place.get("mood_match"):
            score += 0.10

        return round(score, 2)

    def rank_places(self, places: List[Dict]) -> List[Dict]:
        """
        Adds scores to places and returns them sorted by score.
        """

        for place in places:
            place["final_score"] = self.score_place(place)

        return sorted(
            places,
            key=lambda x: x["final_score"],
            reverse=True
        )
