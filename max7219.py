from adafruit_max7219 import bcddigits
import board
import digitalio
from time import sleep
class max:
    def __init__(self):
        cs = digitalio.DigitalInOut(board.D8)


        spi = board.SPI()
        self.display = bcddigits.BCDDigits(spi, cs, nDigits=8)
        self.display.brightness(15)
        self.clear

    def clear(self):
        self.display.clear_all()

    def updateDisplay(self,num : int):
        self.clear()
        #self.display.show_str(0,"{:8}".format(num))
        self.display.show_str(4,"{:1}".format(num))
        self.display.show()

if __name__ =="__main__":
    seg =max()
    for i in range(110):
        seg.clear()
        seg.updateDisplay(i)
        print(i)
        sleep(1)