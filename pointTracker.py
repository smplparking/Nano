from collections import OrderedDict
from scipy.spatial import distance as dist
import numpy as np


class pointTracker:
    def __init__(self, maxDisappeared, maxDistance):
        # Initialize
        self.nextPointID = 0
        self.points = OrderedDict()
        self.disappeared = OrderedDict()
        # num frames to signify object gone
        self.maxDisappeared = maxDisappeared
        # distance between points to signify different objects
        self.maxDistance = maxDistance

    def register(self, centralPoint):
        """
        Registering an object, use next object ID to store central point
        """
        self.points[self.nextPointID] = centralPoint
        self.disappeared[self.nextPointID] = 0
        self.nextPointID += 1

    def deregister(self, pointID):
        """
        # Deregistering an object, delete object from both dictionaries
        """
        del self.points[pointID]
        del self.disappeared[pointID]

    def update(self, boxes):
        """Update centralPoints with new locations
        - if point is gone, increment disappeared frame count

        Args:
            boxes (List(X,Y,X,Y)): list of input bounding boxes

        Returns:
            points (OrderedDict): set of trackable points
        """

        # if no bounding boxes, add disappeared frame count to each point
        if len(boxes) == 0:

            for pointID in list(self.disappeared.keys()):
                self.disappeared[pointID] += 1
                # if object has been gone for too many frames, stop tracking
                if self.disappeared[pointID] > self.maxDisappeared:
                    self.deregister(pointID)
            return self.points

        # Create an array of Central Points all set to 0
        newPoints = np.zeros((len(boxes), 2), dtype="int")

        # loop over the bounding box rectangles
        for (i, (minX, minY, maxX, maxY)) in enumerate(boxes):
            # use the bounding box coordinates to derive the centroid
            cX = int((minX + maxX) / 2.0)
            cY = int((minY + maxY) / 2.0)
            newPoints[i] = (cX, cY)

        # If no points currently tracked, add new tracked points
        if len(self.points) == 0:
            for point in newPoints:
                self.register(point)

        # Currently tracking points, need to match new Points to existing Points
        else:
            # Grab object IDs and Corresponding Central Points
            pointIDs = list(self.points.keys())
            existingPoints = list(self.points.values())

            # Computing the distance between each pair of existing Points and new Points
            pointDistance = dist.cdist(np.array(existingPoints), newPoints)

            # To match, find smallest value in each row, sort the row indexes based on their minimum values
            # so that the row with the smallest value as at the *front* of the index list
            rows = pointDistance.min(axis=1).argsort()

            # Same Process but with Columns and sort with previous row index list
            cols = pointDistance.argmin(axis=1)[rows]

            # Keep track of used Rows/Columns for updating/registering/deregistering
            usedRows = set()
            usedCols = set()

            # Put mother truckers into tuples
            for (row, col) in zip(rows, cols):
                # Ignore already examined row or column
                if row in usedRows or col in usedCols:
                    continue

                # If distance between Central Points is greater than the max distance,
                # do not associate the two central points to the same object

                if pointDistance[row, col] > self.maxDistance:
                    continue

                # Grab pointID for the current row, set its new central point, and reset
                # the disappeared counter
                pointID = pointIDs[row]
                self.points[pointID] = newPoints[col]
                self.disappeared[pointID] = 0

                # update each row and column into our used rows/cols list
                usedRows.add(row)
                usedCols.add(col)

            # Compute row/col index we have **NOT** examined yet
            unusedRows = set(
                range(0, pointDistance.shape[0])).difference(usedRows)
            unusedcols = set(
                range(0, pointDistance.shape[1])).difference(usedCols)

            # if total Central points are >= number of new central points,
            # we need to check and see if some of these objects have possibly disappeared
            if pointDistance.shape[0] >= pointDistance.shape[1]:
                for row in unusedRows:
                    # grab pointID for row index and increment the disappeared counter
                    pointID = pointIDs[row]
                    self.disappeared[pointID] += 1

                    # if objects disappeared frames > max disappeared, we deregister
                    if self.disappeared[pointID] > self.maxDisappeared:
                        self.deregister(pointID)

            # if new central points >  existing central points, register
            # each new input central point as a trackable object
            else:
                for col in unusedcols:
                    self.register(newPoints[col])

        # return the set of trackable points
        return self.points
