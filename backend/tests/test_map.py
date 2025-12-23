# from app.mcp_servers.maps import MapboxMCP

from ..mcp_servers.maps_mcp import MapboxMCP

mcp = MapboxMCP()

# Delhi sample coords — replace yours
# lat = 25.462248
# lng = 81.825512
# lat = 28.613939
# lng = 77.209021
lat = 24.5785
lng = 73.6825

print("🔍 Searching nearby cafes...")
places = mcp.search_places(lat, lng, "Restaurant,cafe,hotel", limit=5)


print("Found:", len(places))

for p in places:
    print(p)


if places:
    # print("\n🚗 Getting travel time...")
    time_data = mcp.get_travel_time(
        origin_lat=lat,
        origin_lng=lng,
        dest_lat=places[0]["latitude"],
        dest_lng=places[0]["longitude"]
    )
    print(time_data)
