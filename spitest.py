from typing import MutableSequence
import board
import busio
import digitalio
from time import sleep
from constants import SevenSegmentASCII
BCD = [63, 6, 91, 79, 102, 109, 125, 7, 127, 111]


# MOSI = digitalio.DigitalInOut(board.MOSI)
# CLK=digitalio.DigitalInOut(board.D6)

# MOSI.direction=digitalio.Direction.OUTPUT
# CLK.direction = digitalio.Direction.OUTPUT


def writeAscii(text):
    out =[]
    for char in text:
        value = SevenSegmentASCII[ord(char)-32]
        spi.write([value])
        spi.write([value])
        sleep(1)
    return out

spi=board.SPI()
writeAscii("Hello World"
)
# while True:
#     for digit in BCD:
#         spi.write([digit])
#         spi.write([digit])
#         sleep(1)
    # spi = board.SPI()
# cs=digitalio.DigitalInOut(board.D6)
# while True:
#     for i in range(10):
#         spi.write([i])
#         sleep(1)