import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

# Create client
client = genai.Client(api_key=GEMINI_API_KEY)

# Supported text model
MODEL_NAME = "gemini-2.5-flash"

def call_gemini(prompt: str) -> str:
    """
    Calls Gemini using the new google.genai SDK
    and enforces JSON-only structured output.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "temperature": 0.2,
            "top_p": 0.9,
            "max_output_tokens": 512,
            "response_mime_type": "application/json"
        }
    )

    if not response.text:
        raise RuntimeError("Empty response from Gemini")

    return response.text.strip()

