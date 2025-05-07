import googlemaps

_API_KEY = "AIzaSyDaMaSBjHby-UNA6_koyEDUYHc45wbR_0c"
_gmaps = googlemaps.Client(key=_API_KEY)

def gmaps_get_locations(coord: list[float], category: str, radius: int) -> list[dict]:
    places = _gmaps.places_nearby(
        location=(coord[0], coord[1]),
        keyword=category,
        radius=radius,
    ).get("results", [])
    parsed_places = []
    for place in places:
        
        parsed_place = {
            "name": place.get("name", "N/A"),
            "rating": f"{place.get("rating", "N/A")} ({place.get("user_ratings_total", "N/A")})",
            "location": [place["geometry"]["location"]["lat"], place["geometry"]["location"]["lng"]],
            "address": place.get("vicinity", "N/A"),
            "link": f"https://www.google.com/maps/search/?api=1&query={place['geometry']['location']['lat']}, {place['geometry']['location']['lng']}"
        }
        parsed_places.append(parsed_place)
    return parsed_places
