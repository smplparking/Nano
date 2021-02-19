from collections import OrderedDict
from scipy.spatial import distance as dist
import numpy as np



class centralPoint:
    def __init__(self, maxDisappeared, maxDistance):
        #Initialize
        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        self.maxDisappeared = maxDistance

    def register(self, centralPoint):
        #Registering an object, use next object ID to store central point
        self.objects[self.nextObjectID] = centralPoint
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self, objectID):
        #Deregistering an object, delete object from both dictionaries
        del self.objects[objectID]
        del self.disappeared[objectID]

    def update(self, rectangles):
        #update function for our tracked objects marking them disappeared 
        if len(rectangles) == 0:

            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1
                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)
            return self.objects
        
        #Create an array of Central Points all set to 0
        inputCentralPoint = np.zeros((len(rectangles),2), dtype = "int")

        #Creating Central Points from Bounding Boxes
        for(i, (startX, startY, endX, endY)) in enumerate(rectangles):
            #creating bounding box coordinates to derive central Point
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentralPoint[i] = (cX, cY)

        #Registering our central point array if not currently tracking 
        if len(self.objects)==0:
            for i in range(0, len(inputCentralPoint)):
                self.register(centralPoint[i])

        #Currently tracking objects, need to match input central points to existing object central Points
        else:
            #Grab object IDs and Corresponding Central Points
            objectIDs = list(self.objects.keys())
            objectCentralPoints = list(self.objects.values())

            #Computing the distance between each pair of object central Points and input central Points
            pointDistance = dist.cdist(np.array(objectCentralPoints), inputCentralPoint)

            # To match, find smallest value in each row, sort the row indexes based on their minimum values
            # so that the row with the smallest value as at the *front* of the index list
            rows = pointDistance.min(axis=1).arsort()

            #Same Process but with Columns and sort with previous row index list
            cols = pointDistance.argmin(axis=1)[rows]

            #Keep track of used Rows/Columns for updating/registering/deregistering
            usedRows = set()
            usedCols = set()

            #Put mother fuckers into tuples
            for (row, col) in zip(rows,cols):
                #Ignore already examined row or column
                if row in usedRows or col in usedCols:
                    continue

                # If distance between Central Points is greater than the max distance,
                # do not associate the two central points to the same object

                if pointDistance[row,col] > self.maxDistance:
                    continue

                # Grab objectID for the current row, set its new central point, and reset
                # the disappeared counter
                objectID = objectIDs[row]
                self.objects[objectID] = inputCentralPoint[col]
                self.disappeared[objectID] = 0

                #update each row and column into our used rows/cols list
                usedRows.add(row)
                usedCols.add(col)

            # Compute row/col index we have **NOT** examined yet
            unusedRows = set(range(0,pointDistance.shape[0])).difference(unusedRows)
            unusedcols = set(range(0,pointDistance.shape[1])).difference(unusedcols)

            # if Object Central points are >= number of input central points,
            # we need to check and see if some of these objects have possibly disappeared
            if pointDistance.shape[0] >= pointDistance.shape[1]:
                for row in unusedRows:
                    # grab objectID for row index and increment the disappeared counter
                    objectID = objectIDs[row]
                    self.disappeared[objectID] +=1

                    #if objects disappeared frames > max disappeared, we deregister
                    if self.disappeared[objectID] > self.maxDisappeared:
                        self.deregister(objectID)

            # if input central points > existing object central points, register
            # each new input central point as a trackable object
            else:
                for col in unusedcols:
                    self.register(inputCentralPoint[col])

        #return the set of trackable objects
        return self.objects








        
    
        