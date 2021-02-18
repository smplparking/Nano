import board

from time import sleep
BCD = [63, 6, 91, 79, 102, 109, 125, 7, 127, 111]


class sevenseg:
    def __init__(self):
        BAUDRATE = 16000000
        #set up SPI using hardware SPI
        self.spi=board.SPI()
        self.spi.try_lock()
        self.spi.configure(baudrate=BAUDRATE)
        self.spi.unlock()


    def us_delay(N):
        sleep(N/1000000.0)


    def ms_delay(N):
        sleep(N/1000.0)


    def reset(self):
        self.spi.write([0x0])
        self.spi.write([0x0])


    async def updateDisplay(self,count):
        # SPI Communication w/ 7segs

        to_send = [count % 10, (count//10) % 10]  # LSD, MSD
        to_send = [BCD[x]
                    for x in to_send]  # use table to convert to binary
        if count > 99:
            to_send = [x + 128 for x in to_send]  # if > 99, add '+'
        await self.spi.write(to_send)  # send spi comms
        await self.spi.write(to_send)  # writing twice fixes segment issues