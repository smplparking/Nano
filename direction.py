import jetson.utils
import dlib
import numpy as np
from database import Database
import max7219
from vehicleDetect import Vehicle
from pointTracker import pointTracker
from commentjson import load
from threading import Thread
from time import strftime
import rfid

rf = rfid.rfid()

GARAGE = "Schrank"
# set up Database
db = Database(GARAGE)

#set up 7seg
seg = max7219.max()
seg.clear()

# Tracked vehicles and corresponding classID
VEHICLES = {3: "car", 8: "truck", }

# Output to MP4?
RECORD = True

# read configuration file
with open("config.json") as conf:
    config = load(conf)

# initialize camera and NN settings
videoIn = "csi://0"
videoInArgs = ["--input-flip=rotate-180"]
date = strftime("%m%d%y")
time = strftime("%H%M%S")
if RECORD:
    videoOut = f"./video/video-{date}-{time}.mp4"
else:
    videoOut = ""
neuralnet = "ssd-mobilenet-v2"
overlay = "box,labels,conf"
threshold = 0.5


# create video sources & outputs
input = jetson.utils.videoSource(videoIn, videoInArgs)
output = jetson.utils.videoOutput(videoOut)

# load the object detection network
import jetson.inference
net = jetson.inference.detectNet(neuralnet, threshold=threshold)

# set up point tracking
pt = pointTracker(
    maxDisappeared=config["max_disappear"], maxDistance=config["max_distance"])
trackers = []
trackedVehicles = {}

tracked_frames = 0
count=db.count
seg.updateDisplay(count)
# process frames until the user exits
while True:
    # capture the next image
    img = input.Capture()
    npimg = jetson.utils.cudaToNumpy(img)
    # if image not captured, something went wrong
    if img is None:
        break

    # resize image (NOTE: necessary?)
    #img = imutils.resize(img, width=config["frame_width"])

    # initialize list of bounding boxes returned by detector
    boxes = []

    if tracked_frames % config["tracking_frames"] == 0:
        tracked_frames = 1
        # initialize trackers
        trackers = []

        # detect objects in the image (with overlay)
        detections = net.Detect(img, overlay=overlay)

        for detection in detections:
            confidence = detection.Confidence

            if confidence < config["confidence"]:
                continue

            if detection.ClassID not in VEHICLES.keys():
                continue

            tracker = dlib.correlation_tracker()
            minX, minY, maxX, maxY = int(detection.Left), int(
                detection.Top), int(detection.Right), int(detection.Bottom)
            bounds = dlib.rectangle(minX, minY, maxX, maxY)
            tracker.start_track(npimg, bounds)
            # add detected vehicle to trackers
            trackers.append(tracker)

    # NOTE: this uses trackers instead of detectors to get higher frame throughput
    else:
        tracked_frames += 1
        for tracker in trackers:
            tracker.update(npimg)
            pos = tracker.get_position()
            # unpack the position object
            minX = int(pos.left())
            minY = int(pos.top())
            maxX = int(pos.right())
            maxY = int(pos.bottom())

            # add the bounding box coordinates to the rectangles list
            boxes.append((minX, minY, maxX, maxY))

            # render the image

    # use point tracker to associate old and new points
    points = pt.update(boxes)
    for (pointID, centerPoint) in points.items():
        vehicle = trackedVehicles.get(pointID, None)

        if vehicle is None:
            vehicle = Vehicle(pointID, centerPoint)
            
        elif not vehicle.tracked:
            if vehicle.direction is None:
                y = [p[0] for p in vehicle.points]
                direction = centerPoint[0] - np.mean(y)
                # NOTE: Make sure direction is correct, otherwise flip gt to lt
                if direction > 0:
                    vehicle.direction = "EXIT"
                    count+=1
                    inc = Thread(target=db.IncDatabase)
                    inc.start()
                elif direction < 0:
                    vehicle.direction = "ENTER"
                    count-=1
                    rfdetect = Thread(target=rf.waitForTag,args=(0x5555,))
                    rfdetect.start()
                    dec = Thread(target=db.DecDatabase)
                    dec.start()
                
                update = Thread(target=seg.updateDisplay,args=(count,))
                update.start()
                # rfdetect = Thread(target=rf.waitForTag(0x5555))
                # rfdetect.start()

                vehicle.tracked = True
            

        trackedVehicles[pointID] = vehicle

    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(
        neuralnet, net.GetNetworkFPS()))

    # print out performance info
    # net.PrintProfilerTimes()
    
    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break
