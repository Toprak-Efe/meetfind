from modules.application import MeetfindApp 
from modules.command import app
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find places near the centroid of friends' locations.")
    parser.add_argument('--file', type=str, default=None, help="The file containing friends' locations (latitude, longitude).")
    parser.add_argument('--type', type=str, default="bar", choices=["cafe", "restaurant", "park", "bar"], help="Type of place to search for (default: cafe).")
    parser.add_argument('--radi', type=int, help="Radius of search from the centroid in kilometers. (default: 20).")
    parser.add_argument('--noui', action="store_true", help="Disable UI and only process the input file.")
    args = parser.parse_args()

    if not args.noui:
        app_gui = MeetfindApp(args.type, args.file, args.radi)
        app_gui.run()
    else:
        app(args.type, args.file, args.radi)
