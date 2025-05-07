import googlemaps

_API_KEY = "AIzaSyDaMaSBjHby-UNA6_koyEDUYHc45wbR_0c"
_gmaps = googlemaps.Client(key=_API_KEY)

def gmaps_get_locations(coord: list[float], category: str, radius: float) -> tuple[bool, list[dict]]:
    try:
        places = _gmaps.places_nearby(
            location=(coord[0], coord[1]),
            keyword=category,
            radius=radius,
        ).get("results", [])
        parsed_places = []
        for place in places:
            parsed_place = {
                "name": place["name"],
                "rating": f"{place["rating"] (place["user_ratings_total"])}",
                "location": [place["geometry"]["location"]["lat"], place["geometry"]["location"]["lon"]],
                "address": place["viccinity"],
                "link": f"https://www.google.com/maps/search/?api=1&query={place['geometry']['location']['lat']},{place['geometry']['location']['lng']}"
            }
            parsed_places.append(parsed_place)
        return True, parsed_places
    except googlemaps.exceptions.ApiError as e:
        return False, []
