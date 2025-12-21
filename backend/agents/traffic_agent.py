# traffic_agent.py adjusts “nearness” using real travel time, not just distance.
# This agent reasons over traffic-adjusted inputs it receives (from Maps MCP / orchestrator) and normalizes them for scoring. 
# app/agents/traffic_agent.py

from typing import Dict, Optional


class TrafficAgent:
    """
    TrafficAgent adjusts distance relevance using
    traffic-aware travel time and simple heuristics.
    """

    def analyze_traffic(
        self,
        place: Dict,
        max_acceptable_time: int = 30
    ) -> Dict:
        """
        Analyzes traffic impact and enriches place data.

        Args:
            place: dict containing travel_time and distance_km
            max_acceptable_time: worst acceptable travel time (minutes)
        """

        travel_time = place.get("travel_time")  # with traffic (minutes)
        base_time = place.get("travel_time_no_traffic")  # optional

        # ---- Determine traffic severity ----
        traffic_level = "low"
        penalty = 0.0

        if base_time and travel_time:
            ratio = travel_time / base_time

            if ratio < 1.3:
                traffic_level = "low"
                penalty = 0.0
            elif ratio < 1.7:
                traffic_level = "medium"
                penalty = 0.2
            else:
                traffic_level = "high"
                penalty = 0.4

        elif travel_time:
            # Fallback: estimate severity using absolute travel time
            if travel_time <= 10:
                traffic_level = "low"
            elif travel_time <= 20:
                traffic_level = "medium"
                penalty = 0.2
            else:
                traffic_level = "high"
                penalty = 0.4

        # ---- Effective travel time ----
        effective_travel_time = travel_time
        if travel_time:
            effective_travel_time = int(travel_time * (1 + penalty))

        # ---- Normalized travel score (0–1) ----
        travel_score = None
        if effective_travel_time is not None:
            travel_score = max(
                0,
                1 - (effective_travel_time / max_acceptable_time)
            )

        return {
            "traffic_level": traffic_level,
            "traffic_penalty": penalty,
            "effective_travel_time": effective_travel_time,
            "travel_score": round(travel_score, 2) if travel_score is not None else None
        }
