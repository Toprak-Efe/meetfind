from modules.geodesics import CentroidPlanner
import numpy as np

def main():
    coords = np.array([
        [70.21, 45.32],
        [70.18, 45.22],
        [70.19, 45.42],
        [70.20, 45.52]
    ])
    planner = CentroidPlanner()
    planner.setCoordinates(coords)
    planner.planCentroid()
    centroid = planner.getCentroid()
    print(centroid)

if __name__ == "__main__":
    main()
