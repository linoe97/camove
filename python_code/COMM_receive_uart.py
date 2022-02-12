import serial 
#from CAM_uart import CAM
from threading import Thread

class READ(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon = True
        self.ser= serial.Serial('COM7',baudrate=115200)
        self.read=None

    def run(self):
        self.read=self.ser.readlines()
        print("LETTURA porta uart",self.reading,".\n")