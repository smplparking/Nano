from time import sleep
import spidev
import Jetson.GPIO as GPIO

# pin definitions
SCK =
BCD = [63, 6, 91, 79, 102, 109, 125, 7, 127, 111]


def getDisplayCode(num):
    return BCD[num]


def us_delay(N):
    sleep(N/1000000.0)


def ms_delay(N):
    sleep(N/1000.0)


def updateDisplay(count):
    # SPI Communication w/ 7segs
    spi = spidev.SpiDev()  # init spi comms
    spi.open(bus, device)  # open spi comms
    to_send = [count % 10, (count//10) % 10]  # LSD, MSD
    if count > 99:
        to_send = [x + 128 for x in to_send]  # if > 99, add '+'
    spi.xfer(to_send)  # send spi comms
    spi.close()  # close spi comms
