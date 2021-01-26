import spidev


def updateDisplay(count):
    # SPI Communication w/ 7segs
    spi = spidev.SpiDev()
    spi.open(bus, device)
    to_send = [0x01, 0x02, 0x03]
    spi.xfer(to_send)
    spi.close()
