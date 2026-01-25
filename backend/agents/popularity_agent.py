from typing import Dict, Optional

class PopularityAgent:
    """
    Estimates how crowded a place is.
    """

    def estimate_crowd(
        self,
        place: Dict,
        time_of_day: Optional[str] = None
    ) -> Dict:

        score = 0.0

        popular_times = place.get("popular_times")
        if popular_times is not None:
            score += popular_times / 100

        rating_count = place.get("user_ratings_total")
        if rating_count:
            if rating_count > 2000:
                score += 0.4
            elif rating_count > 500:
                score += 0.2
            else:
                score += 0.1

        if time_of_day:
            if time_of_day in ["lunch", "afternoon"]:
                score += 0.3
            elif time_of_day in ["evening", "night"]:
                score += 0.4
            else:
                score += 0.1

        score = min(score, 1.0)

        if score < 0.4:
            crowd_level = "low"
        elif score < 0.7:
            crowd_level = "medium"
        else:
            crowd_level = "high"

        return {
            "crowd_level": crowd_level,
            "confidence": round(score, 2)
        }
