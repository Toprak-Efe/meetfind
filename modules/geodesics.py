from abc import abstractmethod
import numpy as np

type Coordinate = list[float]

class Centroid:
    def __init__(self):
        self.coordinates = []

    @abstractmethod
    def getCentroid(self, cords: np.ndarray) -> Coordinate:
        pass

class NaiveCentroid(Centroid):
    def getCentroid(self, cords: np.ndarray) -> Coordinate:
        assert len(cords) > 0, "Centroid requested with less than 0 input coordinates."
        return np.sum(cords, 0)/len(cords) 

class GeodesicCentroids(Centroid): # TO-DO
    def getCentroid(self, cords: np.ndarray) -> Coordinate:
        assert len(cords) > 0, "Centroid requested with less than 0 input coordinates."        
        return [0.0, 0.0] #TO-DO

class CentroidPlanner():
    def __init__(self):
        self._coordinates = np.array([])
        self._planned = False
        self._factory = None

    def setCoordinates(self, cords: np.ndarray):
        assert len(cords.shape) == 2, "Expected a 2-D array."
        assert cords.shape[0] > 0, "Expected more than once coordinate."
        assert cords.shape[1] == 2, "Expected coordinates to have two dimensions."
        if not np.array_equiv(np.sort(self._coordinates, axis=0), np.sort(cords, axis=0)):
            self._planned = False
        self._coordinates = cords

    def addCoordinate(self, cord: Coordinate):
        assert len(cord) == 2, "Expected coordinates with two numbers."
        if cord not in self._coordinates: 
            self._planned = False
        np.append(self._coordinates, cord, axis=0)

    def planCentroid(self):
        if self._planned:
            return
        # Implement best centroid strategy, default is Naive
        # The point with the geodesic centroids is, consider of you're near the poles
        # One guy is on Russia and the other at America, the centroid should be exactly the north pole,
        # But instead it's Finland because we're just averaging coordinates.
        # TIP: Look at the Earth from the top.
        self._factory = NaiveCentroid()
        self._planned = True

    def getCentroid(self) -> Coordinate:
        if not self._planned:
            self.planCentroid()
        assert self._factory is not None, "Expected valid factory, impossible assertion."
        return self._factory.getCentroid(self._coordinates)





