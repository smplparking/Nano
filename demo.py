from datetime import datetime
from time import strftime
import sevenSeg
import database
from commentjson import load
from numpy.core.numeric import False_

from pointTracker import pointTracker
from vehicleDetect import Vehicle

import numpy as np
import dlib
import jetson.inference
import jetson.utils

from database import Database
import asyncio

async def main():
    seg = sevenSeg.sevenseg()
    GARAGE="Schrank"
    db=Database(GARAGE)
    # Tracked vehicles and corresponding classID
    VEHICLES = {3: "car", 8: "truck", }

    # Output to MP4?
    RECORD = True
    CAMERA= True
    # read configuration file
    with open("config.json") as conf:
        config = load(conf)

    # initialize camera and NN settings
    if CAMERA:
        videoIn="csi://0"
        videoInArgs=["--input-flip=rotate-180"]
    else:
        videoIn = "video/test.mp4"
        videoInArgs =["--input-codec=h264"]# 
    date = strftime("%m%d%y")
    time = strftime("%H%M%S")
    if RECORD:
        videoOut = f"video/video-{date}-{time}.mp4"
    else:
        videoOut = ""
    neuralnet = "ssd-mobilenet-v2"
    overlay = "box,labels,conf"
    threshold = 0.3

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

    count = await db.getCurrentCount()
    seg.updateDisplay(count)
    # process frames until the user exits
    while True:

        # capture the next image
        img = input.Capture()
        npimg = jetson.utils.cudaToNumpy(img)
        # if image not captured, something went wrong
        if img is None:
            break

        if logging is False:
            with open(logPath, 'w') as log:
                log.write("Year, Month, Day,        Time, Direction, Avail. Spaces\n")
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
                        count += 1
                        db.IncDatabase()
                    elif direction < 0:
                        vehicle.direction = "ENTER"
                        db.DecDatabase()
                        count -= 1
                    vehicle.tracked = True
            trackedVehicles[pointID] = vehicle

        output.Render(img)

        # update the title bar
        output.SetStatus("{:s} | Network {:.0f} FPS".format(
            neuralnet, net.GetNetworkFPS()))

        # exit on input/output EOS
        if not input.IsStreaming() or not output.IsStreaming():
            break
        seg.updateDisplay(count)
if __name__=="__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())