// Use environment variable for API URL, fallback to localhost for development
const API_BASE = process.env.REACT_APP_API_URL 
  ? `${process.env.REACT_APP_API_URL}/v1`
  : "http://127.0.0.1:8000/api/v1";

export async function fetchPlaces(query, latitude, longitude) {
  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch(`${API_BASE}/places/recommend`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({
        query,
        latitude,
        longitude,
      }),
    });

    if (!response.ok) {
      console.error("API Error:", response.status);
      throw new Error("Failed to fetch recommendations");
    }

    const data = await response.json();
    console.log("API response:", data);

    // 1. FIX: Handle both formats (Direct Array vs { results: [] })
    const placesList = Array.isArray(data) ? data : (data.results || []);

    // 2. Map the data safely
    return placesList.map((p) => ({
      // Use logical OR to ensure we don't crash on missing fields
      id: p.place_id || p.id, 
      name: p.name || "Unknown Place",
      
      // Pass these through so the Booking MCP can use them
      address: p.address,
      website: p.website,
      phone: p.phone,
      
      // Formatting for the UI card
      distance: p.distance_km ? `${p.distance_km} km` : (p.distance || "?"),
      time: p.travel_time ? `${p.travel_time} min` : (p.time || "?"),
      crowd: p.crowd_level || p.crowd || "Unknown",
      price: p.price_level || p.price || "₹₹",
    }));

  } catch (error) {
    console.error("fetchPlaces failed:", error);
    return []; // Return empty array so the app doesn't crash
  }
}