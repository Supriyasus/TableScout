import urllib.parse
from datetime import datetime
from typing import Dict, Any, Optional

class BookingMCP:
    """
    Acts as an Agent Tool that standardizes booking logic across different providers.
    """

    def generate_booking_action(self, place_name: str, address: str, booking_time: str, raw_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Decides the best booking strategy.
        Returns a structured 'Action' object for the client.
        """
        
        # 1. PARSE INTENT
        # Convert string time to object for logic operations
        try:
            dt = datetime.fromisoformat(booking_time.replace('Z', '+00:00'))
            formatted_time = dt.strftime("%Y-%m-%dT%H:%M")
            readable_time = dt.strftime("%I:%M %p")
        except ValueError:
            formatted_time = ""
            readable_time = "requested time"

        # 2. STRATEGY SELECTION (The "Reasoning" Layer)
        
        # Strategy A: Smart Deep Linking for Known Providers
        if raw_url:
            if "opentable" in raw_url:
                # Agentic Behavior: Inject parameters to pre-fill the form
                # Note: These params are illustrative; providers change params often.
                enhanced_url = f"{raw_url}?dateTime={formatted_time}&covers=2"
                return {
                    "status": "handoff",
                    "provider": "OpenTable",
                    "confidence": "high",
                    "action_url": enhanced_url,
                    "message": f"Opening OpenTable for {place_name} at {readable_time}..."
                }
            
            if "resy" in raw_url:
                return {
                    "status": "handoff",
                    "provider": "Resy",
                    "confidence": "high",
                    "action_url": raw_url,
                    "message": f"Redirecting to Resy for {place_name}..."
                }
                
            # Generic Website
            return {
                "status": "handoff",
                "provider": "Direct Website",
                "confidence": "medium",
                "action_url": raw_url,
                "message": f"Checking {place_name}'s official website..."
            }

        # Strategy B: Fallback Search Intent (Construction)
        # If no URL exists, the Agent constructs a search query specifically for 'reservations'
        encoded_query = urllib.parse.quote(f"reservations at {place_name} {address}")
        google_reserve_url = f"https://www.google.com/search?q={encoded_query}"
        
        return {
            "status": "fallback",
            "provider": "Google Search",
            "confidence": "low",
            "action_url": google_reserve_url,
            "message": f"No direct booking link found. Searching reservations for {place_name}..."
        }