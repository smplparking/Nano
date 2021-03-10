import digitalio
import board
from time import sleep


class Bang:
    def __init__(self, cs: digitalio.Pin, frequency=10000000, MOSI=None, CLK=None):
        self.freq = frequency
        self.hz = 1/frequency
        self.cs = digitalio.digitalInOut(cs)
        if MOSI is None or type(MOSI) is not digitalio.Pin:
            self.mosi = board.MOSI
        else:
            self.mosi = MOSI
        if CLK is None or type(MOSI) is not digitalio.Pin:
            self.clk = board.SCLK
        else:
            self.clk = CLK
        self.cs.direction = digitalio.Direction.OUTPUT
        self.clk.direction = digitalio.Direction.OUTPUT
        self.mosi.direction = digitalio.Direction.OUTPUT

    def write_MOSI(self, value):
        self.mosi.value = value == 1

    def write_SCLK(self, value):
        self.clk.value = value == 1

    def write_CS(self, value):
        self.cs.value = value == 1

    def SPI_bang(self, tx):
        '''
         Simultaneously transmit and receive a byte on the SPI.

         Polarity and phase are assumed to be both 0, i.e.:
           - input data is captured on rising edge of SCLK.
           - output data is propagated on falling edge of SCLK.

        '''
        self.write_SCLK(0)
        self.write_CS(0)
        mask = 0x80
        for i in range(8):
            # / * Shift-out a bit to the MOSI line * /
            self.write_MOSI(tx & mask >> i)
            # * Delay for at least the peer's setup time * /
            sleep(self.hz)
            # / * Pull the clock line high * /
            self.write_SCLK(1)
            # / * Delay for at least the peer's hold time * /
            sleep(self.hz)
            # / * Pull the clock line low * /
            self.write_SCLK(0)
        self.write_CS(1)

    def send(self, data):
        self.write_CS(0)
        for i in range(8):
            # // consider leftmost bit
            # // set line high if bit is 1, low if bit is 0
            self.write_MOSI(data & 0x80)

            # // pulse the clock state to indicate that bit value should be read
            self.write_SCLK(0)
            sleep(self.hz)
            self.write_SCLK(1)

            # // shift byte left so next bit will be leftmost
            data <<= 1

        # // deselect device
        self.write_CS(1)
