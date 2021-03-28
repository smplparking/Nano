import digitalio
import board
from time import sleep
BCD = [63, 6, 91, 79, 102, 109, 125, 7, 127, 111]


class Bang:
    def __init__(self, cs: digitalio.Pin, frequency=10000000, MOSI=None, CLK=None):
        self.freq = frequency
        self.period = 1/frequency
        self.cs = digitalio.digitalInOut(cs)
        if MOSI is None or type(MOSI) is not digitalio.Pin:
            self.mosi = board.MOSI
        else:
            self.mosi = MOSI
        if CLK is None or type(CLK) is not digitalio.Pin:
            self.clk = board.SCLK
        else:
            self.clk = CLK
        self.cs.direction = digitalio.Direction.OUTPUT
        self.clk.direction = digitalio.Direction.OUTPUT
        self.mosi.direction = digitalio.Direction.OUTPUT

    def write_MOSI(self, bit):
        '''writes bit to MOSI'''
        self.mosi.value = bit == 1

    def write_SCLK(self, bit):
        self.clk.value = bit == 1

    def write_CS(self, bit):
        self.cs.value = bit == 1

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
        if (bit == 1):
            self.write_MOSI(1)
        else:
            self.write_MOSI(0)

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
        num /= 10
        msd = BCD[num % 10]
        if LARGE:
            msd += 128

        self.SPI_bang(msd)
        self.SPI_bang(lsd)

        self.output()


if __name__ == "__main__":
    seg = Bang(board.D15)
    for i in range(110):
        seg.updateDisplay(i)
