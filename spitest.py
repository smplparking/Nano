from typing import MutableSequence
import board
import busio
import digitalio
from time import sleep
BCD = [63, 6, 91, 79, 102, 109, 125, 7, 127, 111]


# MOSI = digitalio.DigitalInOut(board.MOSI)
# CLK=digitalio.DigitalInOut(board.D6)

# MOSI.direction=digitalio.Direction.OUTPUT
# CLK.direction = digitalio.Direction.OUTPUT

spi=board.SPI()
spi.try_lock()
spi.configure(baudrate=10)
spi.unlock()
while True:
    spi.write([0xff])
    sleep(0.5)
# spi = board.SPI()
# cs=digitalio.DigitalInOut(board.D6)
# while True:
#     for i in range(10):
#         spi.write([i])
#         sleep(1)