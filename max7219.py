from adafruit_max7219 import bcddigits
import board
import busio
import bitbangio
import digitalio
from constants import SevenSegmentASCII
from time import sleep
class max:
    def __init__(self):
        din = board.D10
        clk = board.D11
        cs = digitalio.DigitalInOut(board.D8)

        spi = board.SPI()
        self.display = bcddigits.BCDDigits(spi, cs, nDigits=8)
        self.display.brightness(0)
        self.clear

    def clear(self):
        self.display.clear_all()

    def updateDisplay(self,num : int):
        self.clear()
        self.display.show_str(0,"{:8}".format(num))
        self.display.show()

