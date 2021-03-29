import board
import busio
from time import sleep
BCD = [63, 6, 91, 79, 102, 109, 125, 7, 127, 111]


def us_delay(N):
    """microsecond delay

    Args:
        N (int): sleep for N microseconds
    """
    sleep(N/1000000.0)


def ms_delay(N):
    """millisecond delay

    Args:
        N (int): sleep for N milliseconds
    """
    sleep(N/1000.0)


class sevenseg:
    """ Class for controlling previous team's 7-Seg Display
    """

    def __init__(self, baudrate=16000000, clk=None, din=None, cs=None):
        """ctor for 7-seg, defaults to SPI0 if no pins given

        Args:
            baudrate (int, optional). Defaults to 16000000.
            clk (Pin, optional): clock pin. Defaults to None.
            din (Pin, optional): data in pin. Defaults to None.
            cs (Pin, optional): chip select pin. Defaults to None.
        """
        # set up SPI using hardware SPI
        if clk is None or din is None or cs is None:
            self.spi = board.SPI()
        else:
            self.spi = busio.SPI(clk=clk, mosi=din, cs=cs)
        self.spi.try_lock()
        self.spi.configure(baudrate=baudrate)
        self.spi.unlock()
        self.clear()

    def clear(self):
        """'reset' display by writing 0s
        """
        self.spi.write([0x0])
        self.spi.write([0x0])

    def updateDisplay(self, count):
        """update display with count 
        - up to two numbers shown
        - above 99 shows 99+

        Args:
            count (int): number to display
        """
        # SPI Communication w/ 7segs

        if count > 99:
            count = 99
        
        LSD = count % 10
        MSD = (count//10) % 10

        to_send = [LSD, MSD]  # LSD, MSD
        to_send = [BCD[x]
                   for x in to_send]  # use table to convert to binary
        if count > 99:
            to_send = [x + 128 for x in to_send]  # if > 99, add '+'
        self.spi.write(to_send)  # send spi comms
        self.spi.write(to_send)  # writing twice fixes segment issues
#seg = sevenseg()
#seg.clear()
#seg.updateDisplay(10)