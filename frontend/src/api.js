const API_BASE = "http://127.0.0.1:8000/api/v1";

export async function fetchPlaces(query, latitude, longitude) {
  const token = localStorage.getItem("access_token");

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
    throw new Error("Failed to fetch recommendations");
  }

  const data = await response.json();
  console.log("API response:", data);

  return data.results.map((p) => ({
    id: p.place_id,
    name: p.name,
    rating: p.rating || "N/A",
    distance: p.distance_km ? `${p.distance_km} km` : "?",
    time: p.travel_time ? `${p.travel_time} min` : "?",
    crowd: p.crowd_level || "Unknown",
    price: "₹₹",
    reason: p.explanation,
  }));
}
