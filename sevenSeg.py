import spidev
from time import sleep
BCD = [63, 6, 91, 79, 102, 109, 125, 7, 127, 111]
spi = spidev.SpiDev()  # init spi comms

bus = 0
device = 0
bigboard = False


def getDisplayCode(num):
    return BCD[num]


def us_delay(N):
    sleep(N/1000000.0)


def ms_delay(N):
    sleep(N/1000.0)


def reset():
    spi.open(bus, device)
    spi.xfer([0x81])


def updateDisplay(count):
    # SPI Communication w/ 7segs
    spi.open(0, 0)  # open spi comms
    if not bigboard:
        spi.xfer([0x76])  # clear display
    to_send = [count % 10, (count//10) % 10]  # LSD, MSD
    if bigboard:
        to_send = [getDisplayCode(x)
                   for x in to_send]  # use table to convert to binary
    if count > 99 and bigboard:
        to_send = [x + 128 for x in to_send]  # if > 99, add '+'
    spi.xfer(to_send)  # send spi comms
    spi.close()  # close spi comms


reset()

for i in range(100):
    print(f'displaying {i}')
    updateDisplay(i)
    sleep(5)
