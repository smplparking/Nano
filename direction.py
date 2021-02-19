from datetime import datetime
import os
from threading import Thread
from time import strftime

from commentjson import load

from pointTracker import pointTracker
from vehicleDetect import Vehicle
from sevenSeg import sevenseg

import jetson.inference
import jetson.utils

# Tracked vehicles and corresponding classID
VEHICLES = {3: "car", 8: "truck", }

# Output to MP4?
RECORD = False

# read configuration file
with open("config.json") as conf:
    config = load(conf)

# initialize camera and NN settings
videoIn = "csi://0"
videoInArgs = ["--input-flip=rotate-180"]
date = strftime("%m%d-%H%M%S")
if RECORD:
    videoOut = f"./video/video-{date}.mp4"
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

# set up height and width for bounding box
H = None
W = None

# set up point tracking
pt = pointTracker(
    maxDisappeared=config["max_dissapear"], maxDistance=config["max_distance"])
trackers = []
trackedVehicles = {}


# total frames processed ? NOTE: MAYBE UNNECCESARY
totalFrames = 0


logFile = None

# fps throughput estimator
fps = FPS().start()

# process frames until the user exits
while True:

    # if TEST:
    #     miniseg.write(count)
    # else:
    #     seg.updateDisplay(count)

    # capture the next image
    img = input.Capture()

    # ts=datetime.now()
    newDate = strftime("%m-%d-%y")

    # if image not captured, something went wrong
    if img is None:
        break

    if logFile is None:
        logPath = f"./logs/{date}.log"
        pos = logFile.seek(0, os.SEEK_END)
        with open(logPath, 'a') as log:
            log.write("Year, Month, Day, Time, Direction")

    # resize image
    img = imutils.resize(img, width=config["frame_width"])

    #rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # NOTE: IDK wtf this does, but CV2 doesn't work... find an alt in inference

    # set image dimensions
    if W is None or H is None:
        (H, W) = img.shape[:2]
        # foot per pixel set in config file/ divided by height (we go up/down)
        footPerPixel = conf["distance"]/H

    # initialize list of bounding boxes returned by detector
    boxes = []

    # NOTE: IGNORING THE TRACKER AND JUST USING CV, MIGHT NEED TO REVISIT
    # if totalFrames % config["tracking_frames"] == 0

    # initialize trackers
    trackers = []

    # detect objects in the image (with overlay)
    detections = net.Detect(img, overlay=overlay)

    for detection in detections:
        confidence = detection.Confidence
        centerPoint = detection.Center
        if detection.ClassID not in VEHICLES.keys():
            continue
        # NOTE: no idea wtf they're doing here, lets find an easier
        # way to do this with our tools at hand
        # tracker = dlib.correlation_tracker()
        # rect = dlib.rectangle(startX, startY, endX, endY)
        # tracker.start_track(rgb, rect)

        # add the tracker to our list of trackers so we can
        # utilize it during skip frames
        # trackers.append(tracker)
        # NOTE: left here for the night... gotta figure out what exactly
        # they're adding to the trackers list, our way is easier since we
        # already have center
        # do this if the vehicle hasn't been counted
        # count = db.updateDatabase(GARAGE)
        # if TEST:
        #     miniseg.write(count)
        # else:
        #     seg.updateDisplay(count)
        # print(
        #     f'{VEHICLES[detection.ClassID]} detected, count is now {count}')
    # render the image
    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(
        neuralnet, net.GetNetworkFPS()))

    # print out performance info
    net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break
