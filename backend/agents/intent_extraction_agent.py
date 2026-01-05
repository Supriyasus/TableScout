import json
from schemas.user_intent import UserIntent
from agents.gemini_client import call_gemini


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

Rules:
- Do NOT restrict vocabulary
- Do NOT invent information
- Be conservative with scores
- Output ONLY valid JSON
- Do NOT add explanations or markdown
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
            # Gemini sometimes returns ```json blocks — strip them safely
            cleaned = raw_output.strip().removeprefix("```json").removesuffix("```").strip()
            return UserIntent.model_validate_json(cleaned)

        except Exception as e:
            raise ValueError(
                f"Invalid intent JSON returned by Gemini:\n{raw_output}"
            ) from e
