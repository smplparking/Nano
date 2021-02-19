from adafruit_max7219 import bcddigits
import board
import busio
import bitbangio
import digitalio


class max:
    def __init__(self):
        din = board.D10
        clk = board.D11
        cs = digitalio.DigitalInOut(board.D8)

        spi = board.SPI()
        self.display = bcddigits.BCDDigits(spi, cs, nDigits=8)
        self.display.brightness(0)

    def write(self,num):
        self.display.clear_all()
        self.display.show_str(0,"{:8}".format(num))
        self.display.show()

m=max()
m.write(123)
