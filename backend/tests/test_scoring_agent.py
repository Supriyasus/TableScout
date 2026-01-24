from backend.agents.scoring_agent import ScoringAgent
from backend.schemas.user_intent import UserIntent

def make_intent():
    return UserIntent(
        query="I want a calm cozy place to hang out with good food",
        categories=["cafe", "restaurant"],
        min_rating=3.5,
        max_travel_time=30,
        crowd_preference="medium"
    )

def test_score_place_with_user_preferences_boost():
    agent = ScoringAgent()
    intent = make_intent()

    place = {
        "name": "Test Cafe",
        "category": "cafe",
        "rating": 4.0,
        "travel_time": 15,
        "crowd_level": "medium"
    }

    user_preferences = {
        "place_type_affinity": {
            "cafe": 0.9
        }
    }

    score_without = agent.score_place(
        place=place,
        intent=intent,
        user_preferences=None
    )

    score_with = agent.score_place(
        place=place,
        intent=intent,
        user_preferences=user_preferences
    )

    assert score_with > score_without
