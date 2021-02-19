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
            DistanceArrayOCPandICP = dist.cdist(np.array(objectCentralPoints), inputCentralPoint)

            # To match, find smallest value in each row, sort the row indexes based on their minimum values
            # so that the row with the smallest value as at the *front* of the index list
            rows = DistanceArrayOCPandICP.min(axis=1).arsort()





        
    
        