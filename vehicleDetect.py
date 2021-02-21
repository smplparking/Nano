class Vehicle:
    def __init__(self, pointID, centralPoint):
        # store the object ID, then initialize a list of centroids
        # using the current centroid
        self.pointID = pointID
        self.points = [centralPoint]

        # initialize two booleans, (1) used to indicate if the
        # object's speed has already been estimated or not, and (2)
        # used to indidicate if the object's speed has been logged or
        # not
        self.tracked = False
        # initialize the direction of the object
        self.direction = None
