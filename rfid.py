import board
import digitalio
import busio
from time import sleep
import serial
from sendemail import sendEmail

class rfid:
    def __init__ (self):
        self.uart = serial.Serial("/dev/ttyTHS1",baudrate=19900,timeout=5)
        self.bytes=0
    def read(self):
        self.bytes=int.from_bytes(self.uart.read(),"big") << 8
        self.bytes+=int.from_bytes(self.uart.read(),"big")
        #print(self.bytes)
        #self.bytes=0

    def tagExists(self,tag):
        if tag == self.bytes:
            return True
        else:
            sendEmail()
            return False         

    def waitForTag(self,tag):
        print("waiting for tag")
        self.read()
        return self.tagExists(tag)

if __name__ == "__main__":
    rf = rfid()
    while True:
        if rf.waitForTag(0x5555):
            print("got tag")
        else:
            print("sending email")
