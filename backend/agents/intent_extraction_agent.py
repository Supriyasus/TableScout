import re
from backend.schemas.user_intent import UserIntent
from backend.agents.gemini_client import call_gemini


def extract_json(text: str) -> str:
    """
    Extract the first valid JSON object from LLM output.
    Handles partial / noisy responses safely.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in LLM output")
    return match.group(0)


def fallback_intent() -> UserIntent:
    """
    Safe fallback intent if LLM fails.
    Ensures system never crashes.
    """
    return UserIntent(
        descriptors=[],
        preferences={},
        place_types=["restaurant", "cafe"],
        constraints=[],
        time_of_day=None,
        booking_required=False
    )


class IntentExtractionAgent:
    """
    Converts natural language user input into structured intent.
    This is the ONLY LLM-powered agent in the system.
    """

    SYSTEM_PROMPT = """
You are an intent extraction agent.

Your task:
1. Extract descriptive phrases exactly as the user says them.
2. Project them into abstract preference dimensions with values between 0 and 1.
3. Infer suitable place types ONLY from the allowed list below.

Allowed place_types (choose ONLY from these):
- restaurant
- cafe
- bar
- lounge
- bakery
- fast_food
- food_court
- ice_cream

Rules:
- Do NOT restrict vocabulary for descriptors
- Do NOT invent information
- Be conservative with scores
- place_types MUST be chosen ONLY from the allowed list
- If no place type clearly applies, return ["restaurant"]
- Never return generic values like "place", "spot", or "location"
- Output ONLY valid JSON
- Do NOT add explanations, markdown, or comments
"""

    def extract(self, user_query: str) -> UserIntent:
        prompt = f"""
{self.SYSTEM_PROMPT}

Return JSON strictly in this format:

{{
  "descriptors": string[],
  "preferences": {{ "<dimension>": number }},
  "place_types": string[],
  "constraints": string[],
  "time_of_day": string | null,
  "booking_required": boolean
}}

User query:
"{user_query}"
"""

        raw_output = call_gemini(prompt)

        try:
            json_text = extract_json(raw_output)
            return UserIntent.model_validate_json(json_text)

        except Exception as e:
            # IMPORTANT: never crash the system
            # Log raw_output in real systems
            return fallback_intent()
