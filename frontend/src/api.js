export async function fetchPlaces(query) {
  console.log("User query:", query);

  // Simulate AI + MCP processing
  await new Promise((r) => setTimeout(r, 1000));

  return [
    {
      id: 1,
      name: "Blue Tokai",
      rating: 4.5,
      distance: "700m",
      time: "8 min",
      crowd: "Low",
      price: "₹₹",
      reason: "Quiet during evenings, affordable, low crowd at 5 PM",
    },
    {
      id: 2,
      name: "Third Wave Coffee",
      rating: 4.3,
      distance: "1.2 km",
      time: "10 min",
      crowd: "Medium",
      price: "₹₹",
      reason: "Good ambience but slightly busy after 6 PM",
    },
  ];
}
