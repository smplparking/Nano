class Vehicle:
    def __init__(self, pointID, centralPoint):
       
        
        # store the object ID, then initialize a list of centroids
        # using the current centroid
        self.pointID = pointID
        self.points = [centralPoint]
        
        # initialize boolean
        # used to indidicate if the object's direction has been logged or
        # not
        self.tracked = False
        # initialize the direction of the object
        self.direction = None
    def __del__():
        print("im gone")