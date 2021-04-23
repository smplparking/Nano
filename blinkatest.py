import board
import digitalio
import busio
print("hello blinka!")
print("board contents: ", dir(board))
pin = digitalio.DigitalInOut(board.D4.OUT)
print("Digital IO ok!")

i2c = busio.I2C(board.SCL, board.SDA)
print("I2C ok!")
i2c = busio.I2C(board.SCL_1, board.SDA_1)
print("I2C_1 ok!")

spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
print("SPI ok!")
print("done!")