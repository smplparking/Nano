from datetime import datetime
from threading import Thread
from time import strftime

from commentjson import load
from numpy.core.numeric import False_

from pointTracker import pointTracker
from vehicleDetect import Vehicle
from sevenSeg import sevenseg
import max7219
from database import Database

import numpy as np
import dlib
import jetson.inference
import jetson.utils

# set up Database
db = Database()
GARAGE = "Schrank"
count = db.getCurrentCount(GARAGE)

# set up 7 seg
bigboard = False
if bigboard:
    seg = sevenseg()
else:
    seg=max7219.max()
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
time= strftime("%H%M%S")
if RECORD:
    videoOut = f"./video/video-{date}-{time}.mp4"
else:
    videoOut = ""
neuralnet = "ssd-mobilenet-v2"
overlay = "box,labels,conf"
threshold = 0.5

# load the object detection network
net = jetson.inference.detectNet(neuralnet, threshold=threshold)

# create video sources & outputs
input = jetson.utils.videoSource(videoIn, videoInArgs)
output = jetson.utils.videoOutput(videoOut)

# set up point tracking
pt = pointTracker(
    maxDisappeared=config["max_disappear"], maxDistance=config["max_distance"])
trackers = []
trackedVehicles = {}

# set up logging
logPath = f"./logs/{date}.log"
logging = False

tracked_frames = 0
seg.updateDisplay(count)
# process frames until the user exits
while True:
    #seg.updateDisplay(count)    

    # if TEST:
    #     miniseg.write(count)
    # else:
    #     seg.updateDisplay(count)

    # capture the next image
    img = input.Capture()
    npimg = jetson.utils.cudaToNumpy(img)
    # if image not captured, something went wrong
    if img is None:
        break
    
    if logging is False:
        with open(logPath, 'w') as log:
                log.write("Year, Month, Day, Time, Direction\n")
        logging = True

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
            # centerPoint = detection.Center

            if confidence < config["confidence"]:
                continue

            if detection.ClassID not in VEHICLES.keys():
                continue

            tracker = dlib.correlation_tracker()
            minX, minY, maxX, maxY = int(detection.Left), int(detection.Top), int(detection.Right), int(detection.Bottom)
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
                    vehicle.direction = "ENTER"
                    count = db.IncDatabase(GARAGE)
                elif direction < 0:
                    vehicle.direction = "EXIT"
                    count = db.DecDatabase(GARAGE)
                vehicle.tracked = True
            seg.updateDisplay(count)
        trackedVehicles[pointID] = vehicle

        if not vehicle.logged:
            with open(logPath, 'a') as log:
                log.write(
                    f"{strftime('%Y, %b, %d, %I:%M:%S %p')}, {vehicle.direction}\n")
            vehicle.logged = True

    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(
        neuralnet, net.GetNetworkFPS()))

    # print out performance info
    #net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break
