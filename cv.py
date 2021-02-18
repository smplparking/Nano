#!/usr/bin/python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import database
import sevenSeg

import jetson.inference
import jetson.utils
from time import strftime
import argparse
import sys

# initialize camera and NN settings
videoIn = "csi://0"
date = strftime("%m%d-%H%M%S")
videoOut = f"./video/video-{date}.mp4"
neuralnet = "ssd-mobilenet-v2"
overlay = "box,labels,conf"
threshold = 0.5


# init database
db = database.Database()
GARAGE = "Admin"
count = db.getCurrentCount()

# init 7seg
seg = sevenSeg.sevenseg()
seg.updateDisplay(count)

# load the object detection network
net = jetson.inference.detectNet(neuralnet, threshold=threshold)

# create video sources & outputs
input = jetson.utils.videoSource(videoIn)
output = jetson.utils.videoOutput(videoOut)

# process frames until the user exits
while True:
    # capture the next image
    img = input.Capture()

    # detect objects in the image (with overlay)
    detections = net.Detect(img, overlay=overlay)

    # print the detections
    print("detected {:d} objects in image".format(len(detections)))

    for detection in detections:
        if detection == 'car':
            count = db.updateDatabase(GARAGE)
            seg.updateDisplay(count)
            print(f'{detection} detected, count is now {count}')
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
