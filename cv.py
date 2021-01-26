#!/usr/bin/python
#
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
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

from database import updateDatabase
from sevenSeg import updateDisplay

import jetson.inference
import jetson.utils
import asyncio
import database.py
import sys
import time

import


async def countVehicles():
    vehiclecount = 0  # Allocate memory for Vehicle Count

    network = "ssd-mobilenet-v2"  # Use pre-trained NN for vehicle detection
    threshold = 0.5  # change this to affect triggering threshold
    cam = "/dev/video0"  # might need to change this to CSI, depending
    cWidth = 640
    cHeight = 480  # 640x480 may need to adjust for compromise b/w speed and clarity

    # load the object detection network
    net = jetson.inference.detectNet(network, sys.argv, threshold)

    font = jetson.utils.cudaFont()
    # create the camera
    camera = jetson.utils.gstCamera(cWidth, cHeight, cam)

    # process frames until user exits
    t = time.time()
    while True:
        # capture the image
        img, width, height = camera.CaptureRGBA(zeroCopy=1)

        # detect objects in the image (with overlay)
        detections = net.Detect(img, width, height, False)

        ####
        #  Looks like we should have a if statement: If detections = vehicle, update database counter
        #                                               else: ignore detections
        # -Josh

        ####
        # Probably need vehicle fronts/ backs to inc/decrement :cry:
        for detection in detections:
            if detection == 'vehicle':
                vehicleCount = updateDatabase(u'Shrank')
                updateDisplay(vehicleCount)
                print('Vehicle Detected')

        # net.PrintProfilerTimes()

# Nano's Capability
# 2 Uart
# 2 I2C
# 2 SPI

# Nano Comms
# rx info from MM about RFID cars
# tx info to MM about Photo cars, to update 7-seg


# Main Module
# 1 SPI 7-segment
# 1 UART?? RFID comms
#
