from textual.widgets import RichLog
import googlemaps

_API_KEY = "AIzaSyDaMaSBjHby-UNA6_koyEDUYHc45wbR_0c"
_gmaps = googlemaps.Client(key=_API_KEY)

def gmaps_get_locations(coord: list[float], category: str, logger: RichLog) -> tuple[bool, list[dict]]:
    try:
        places = _gmaps.places_nearby(
            location=(coord[0], coord[1]),
            keyword=category,
            radius=20,
        ).get("results", [])
        logger.write(f"Type: {places[0]}")
        return False, []
    except googlemaps.exceptions.ApiError as e:
        logger.write(f"Unable to fetch locations. {e}")
        return False, []

locations = [
    {
        "name": "Baydoner",
        "address": "Tekirdag, Esentepe, bilmem ne",
        "score": "4.6 (960)",
        "image": "asdasdas.com/jpg",
        "link": "asdasdasd.com"
    }
]

