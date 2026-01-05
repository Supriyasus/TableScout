import requests
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
if not MAPBOX_TOKEN:
    raise RuntimeError("MAPBOX_TOKEN not set")

# MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
# MAPBOX_TOKEN = "pk.eyJ1IjoicHJhdHl1c2hkdWJlIiwiYSI6ImNtamlxYW1xZTFvemIzZHM2Y2k2ZTN5ZjYifQ._HVSCVKGv8V4GiVD6PFH1w"

class MapboxMCP:

    GEOCODE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
    DIRECTIONS_URL = "https://api.mapbox.com/directions/v5/mapbox/driving-traffic"

    def search_places(
        self,
        lat: float,
        lng: float,
        category: str,
        limit: int = 15
    ):
        url = f"https://api.mapbox.com/search/v1/category/{category}"

        params = {
            "proximity": f"{lng},{lat}",   # NOTE lng,lat
            "limit": limit,
            "language": "en",
            "access_token": MAPBOX_TOKEN
        }

        res = requests.get(url, params=params, timeout=5)
        res.raise_for_status()
        data = res.json()

        features = data.get("features")
        if not isinstance(features, list):
            return []

        places = []

        for f in data.get("features", []):
            coords = f["geometry"]["coordinates"]
            props = f.get("properties", {})

            places.append({
                "place_id": props.get("mapbox_id") or f.get("id"),
                "name": props.get("feature_name") or props.get("name"),
                "address": props.get("place_name") or props.get("description"),
                "latitude": coords[1],
                "longitude": coords[0],
                "categories": props.get("poi_category") or [],
                "rating": None,              # placeholder (future)
                "user_ratings_total": None,  # placeholder
                "price_level": None          # placeholder
            })

        return places



    def get_travel_time(
        self,
        origin_lat: float,
        origin_lng: float,
        dest_lat: float,
        dest_lng: float
    ) -> Dict:
        """
        Get ETA + distance using Mapbox Traffic Directions
        """

        url = (
            f"{self.DIRECTIONS_URL}/"
            f"{origin_lng},{origin_lat};{dest_lng},{dest_lat}"
        )

        params = {
            "geometries": "geojson",
            "overview": "simplified",
            "access_token": MAPBOX_TOKEN
        }

        res = requests.get(url, params=params, timeout=5)
        res.raise_for_status()
        data = res.json()

        routes = data.get("routes")
        if not routes:
            raise RuntimeError("No routes returned by Mapbox")

        route = routes[0]

        return {
            "distance_km": round(route["distance"] / 1000, 2),
            "travel_time": int(route["duration"] // 60)  # min
        }
