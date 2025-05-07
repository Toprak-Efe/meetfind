from modules.application import MeetfindApp 
import argparse
import os
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find places near the centroid of friends' locations.")
    parser.add_argument('--file', type=str, default=None, help="The file containing friends' locations (latitude, longitude).")
    parser.add_argument('--type', type=str, default="bar", choices=["all", "cafe", "restaurant", "park", "bar"], help="Type of place to search for (default: cafe).")
    parser.add_argument('--noui', action="store_true", help="Disable UI and only process the input file.")
    args = parser.parse_args()

    coordinates = []
    search_type = args.type
    
    err = False
    if args.file is not None:
        if os.path.exists(args.file):
            with open(args.file, "r") as f:
                def parse_coordinate(input) -> tuple[bool, list[float]]:
                    pattern = r"^\s*(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)\s*$"
                    match = re.match(pattern, input)
                    if match:
                        lat_str, lon_str = match.groups()
                        lat = float(lat_str)
                        lon = float(lon_str)
                        return (True, [lat, lon])
                    else:
                        return (False, [])
                for line in f.readlines():
                    line = line.strip()
                    ret, cords = parse_coordinate(line)
                    if ret:
                        coordinates.append(cords)
        else:
            if args.noui:
                print(f"ERROR: Unable to find file at {args.file}")
                exit(1)

    if not args.noui:
        app = MeetfindApp(coordinates, search_type)
        app.run()
    else:
        pass
