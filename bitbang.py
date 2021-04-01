import digitalio
import board
from time import sleep
BCD = [63, 6, 91, 79, 102, 109, 125, 7, 127, 111]


class Bang:
    def __init__(self, cs= None, frequency=10000000, MOSI=None, CLK=None):
        self.freq = frequency
        self.period = 1/frequency
        self.cs = digitalio.DigitalInOut(board.CE0)
        self.mosi=digitalio.DigitalInOut(board.MOSI)
        self.clk = digitalio.DigitalInOut(board.D11)
        self.cs.switch_to_output()
        self.mosi.switch_to_output()
        self.clk.switch_to_output()

    def write_MOSI(self, bit):
        '''writes bit to MOSI'''
        self.mosi.value = bit

    def write_SCLK(self, bit):
        self.clk.value = bit

    def write_CS(self, bit):
        self.cs.value = bit 

    def tick(self):
        self.write_SCLK(0)
        sleep(self.period)
        self.write_SCLK(1)

    def SPI_bang(self, data, debug=False):
        '''break byte of data into bits and calls send on each'''
        mask = 0x80
        for i in range(8):
            bit = (data & mask) >> 7
            self.send(bit, debug)
            data <<= 1
            sleep(self.period)

    def send(self, bit, debug=False):
        ''' send bit to MOSI, then clock lo/hi'''
        self.write_MOSI(bit)

        self.tick()

        if debug:
            sleep(1)

    def output(self):
        ''' toggles CS pin low then high '''
        self.write_CS(0)
        sleep(self.period)
        self.write_CS(1)

    def clear(self):
        """clear display"""
        self.SPI_bang(0)
        self.SPI_bang(0)

    def updateDisplay(self, num):
        ''' takes a number and writes to 7-seg'''
        LARGE = False
        if num > 99:
            num = 99
            LARGE = True

        lsd = BCD[num % 10]
        msd = BCD[num//10 % 10]
        if LARGE:
            msd += 128

        self.SPI_bang(msd)
        self.SPI_bang(lsd)

        self.output()

    def sendOne(self,data):
        
        mask = 0x80
        for i in range(8):
            self.write_CS(0)
            bit = (data & mask) >> 7
            self.send(bit)
            data <<= 1
            sleep(self.period)
            self.write_CS(1)

if __name__ == "__main__":
    seg = Bang(board.CE0)
    for i in range(110):
        seg.sendOne(i)
        print(i)
        sleep(1)            