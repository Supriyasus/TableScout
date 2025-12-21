#Detect booking intent, Ensure user confirmation, Ensure required details (time, people), Prepare a safe booking request, Delegate execution to Booking MCP
from typing import Dict, Optional

class BookingAgent:
    """
    BookingAgent is responsible for deciding whether a booking
    can proceed and preparing a safe, structured booking request.

    It DOES NOT execute the booking itself.
    """

    def evaluate_booking_state(
        self,
        selected_place: Optional[Dict],
        booking_time: Optional[str],
        people_count: Optional[int],
        user_confirmed: bool
    ) -> Dict:
        """
        Determines the current booking state and what action is required next.
        """

        # 1. No place selected
        if not selected_place:
            return {
                "status": "error",
                "message": "No place has been selected for booking."
            }

        # 2. Missing booking time
        if not booking_time:
            return {
                "status": "need_info",
                "field": "time",
                "question": "At what time should I book the table?"
            }

        # 3. Missing number of people
        if not people_count:
            return {
                "status": "need_info",
                "field": "people",
                "question": "For how many people should I book the table?"
            }

        # 4. Explicit confirmation required
        if not user_confirmed:
            return {
                "status": "need_confirmation",
                "question": (
                    f"Should I proceed with booking a table at "
                    f"{selected_place.get('name')} for {people_count} "
                    f"people at {booking_time}?"
                )
            }

        # 5. Ready to book
        return {
            "status": "ready"
        }

    def build_booking_payload(
        self,
        selected_place: Dict,
        booking_time: str,
        people_count: int,
        user_name: str,
        user_contact: Optional[str] = None
    ) -> Dict:
        """
        Builds a structured booking payload to be sent to the Booking MCP Server.
        """

        return {
            "restaurant_name": selected_place.get("name"),
            "address": selected_place.get("address"),
            "place_id": selected_place.get("place_id"),
            "time": booking_time,
            "people": people_count,
            "user_name": user_name,
            "contact": user_contact
        }
