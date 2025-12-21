# estimates how crowded a place is at a given time and converts raw signals into a simple, explainable crowd level.
# app/agents/popularity_agent.py

from typing import Dict, Optional


class PopularityAgent:
    """
    PopularityAgent estimates how crowded a place is
    using available popularity signals and heuristics.
    """

    def estimate_crowd(
        self,
        place: Dict,
        time_of_day: Optional[int] = None
    ) -> Dict:
        """
        Estimates crowd level: low / medium / high.
        """

        score = 0.0

        # 1. Popular times signal (if available)
        popular_times = place.get("popular_times")  # 0–100
        if popular_times is not None:
            score += popular_times / 100  # normalize to 0–1

        # 2. Review density heuristic
        rating_count = place.get("user_ratings_total")
        if rating_count:
            if rating_count > 2000:
                score += 0.4
            elif rating_count > 500:
                score += 0.2
            else:
                score += 0.1

        # 3. Time-of-day heuristic
        if time_of_day is not None:
            if 12 <= time_of_day <= 14:
                score += 0.3  # lunch rush
            elif 18 <= time_of_day <= 21:
                score += 0.4  # evening rush
            else:
                score += 0.1

        # ---- Normalize score ----
        score = min(score, 1.0)

        # ---- Determine crowd level ----
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
