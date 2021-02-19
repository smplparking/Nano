class Vehicle:
    def __init__(self, pointID, centralPoint):
        # store the object ID, then initialize a list of centroids
        # using the current centroid
        self.pointID = pointID
        self.points = [centralPoint]

        # initialize a dictionaries to store the timestamp and
        # position of the object at various points
        self.timestamp = {"A": 0, "B": 0, "C": 0, "D": 0}
        self.position = {"A": None, "B": None, "C": None, "D": None}
        self.lastPoint = False

        # initialize two booleans, (1) used to indicate if the
        # object's speed has already been estimated or not, and (2)
        # used to indidicate if the object's speed has been logged or
        # not
        self.tracked = False
        # initialize the direction of the object
        self.direction = None
