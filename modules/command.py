from modules.geodesics import CentroidPlanner
from modules.maps import gmaps_get_locations
from tabulate import tabulate
import os

def app(category, file, radi):
    assert file, "ERROR: File argument is required with --nogui. Please enter the file argument."
    assert os.path.exists(file), f"ERROR: Unable to open file at {os.path.abspath(file)}"
    if not radi:
        radi = 400
    assert radi > 0, "ERROR: Invalid radi argument, expected a positive integer."
    if not category:
        category = "bar"
    
    coordinates = []
    with open(file, "r") as f:
        def parse_coordinate(line_text: str) -> tuple[bool, list[float]]:
            sectors = line_text.split(',')
            try:
                lat, lon = float(sectors[0]), float(sectors[1])
                return True, [lat, lon]
            except Exception:
                lat, lon = 0.0, 0.0
                return False, [lat, lon]
        for line in f:
            line = line.strip()
            ret, cords = parse_coordinate(line)
            if ret:
                coordinates.append(cords)
    assert len(coordinates) > 0, "ERROR: Expected coordinates in the input file."

    results = []
    planner = CentroidPlanner()
    planner.setCoordinates(coordinates)
    centroid = planner.getCentroid()
    try:
        results = gmaps_get_locations(centroid, category, radi)
    except Exception as e:
        print(f"ERROR: Unable to get locations. {e}")
        return
    if len(results) == 0:
        print(f"Unable to find any results for given parameters.")
    # Fine print results
    header = results[0].keys()
    rows = [x.values() for x in results]
    print(tabulate(rows, header, tablefmt="fancy_grid"))
    
