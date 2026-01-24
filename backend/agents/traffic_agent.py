from typing import Dict

class TrafficAgent:
    """
    Normalizes travel time using traffic heuristics.
    """

    def analyze_traffic(
        self,
        place: Dict,
        max_acceptable_time: int = 30
    ) -> Dict:

        travel_time = place.get("travel_time")
        base_time = place.get("travel_time_no_traffic")

        penalty = 0.0
        traffic_level = "low"

        if base_time and travel_time:
            ratio = travel_time / base_time
            if ratio > 1.7:
                traffic_level = "high"
                penalty = 0.4
            elif ratio > 1.3:
                traffic_level = "medium"
                penalty = 0.2

        effective_time = travel_time
        if travel_time:
            effective_time = int(travel_time * (1 + penalty))

        travel_score = None
        if effective_time:
            travel_score = max(0, 1 - effective_time / max_acceptable_time)

        return {
            "traffic_level": traffic_level,
            "travel_time": effective_time,
            "travel_score": round(travel_score, 2) if travel_score else None
        }
