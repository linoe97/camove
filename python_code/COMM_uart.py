import serial 
from CAM_uart import CAM
from threading import Thread

class COMM(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon = True
        self.ser= serial.Serial('COM3',baudrate=115200)
        self.dev=(0,0)  #set deviation
        self.message=None #set variables
        self.buffer=None
        self.reading=None

    def set_camera(self,cam):
        self.camera=cam 

    def run(self):
        self.set_zero()
        print("Conferma messaggio scritto ",self.message,". ",len(self.message)," ",self.buffer)
        while self.camera.cam.isOpened(): 
            if self.camera.bbox is not None:
                self.dev=self.camera.deviation()                    
                print("Deviation X: ",self.dev[0]," Y: ",self.dev[1])
                if self.dev[0]==320:
                    self.dev[0]=0
                if self.dev[1]==240:
                    self.dev[1]=0
                print("Lenght X: ",len(str(self.dev[0]))," Lenght Y: ",len(str(self.dev[1])))
                self.message=str(len(str(self.dev[0])))+str(len(str(self.dev[1])))+str(self.dev[0])+str(self.dev[1])
                print("Messaggio: ",self.message)
                while len(self.message)<10:
                    self.message=self.message+"."
                self.buffer=self.message.encode('utf-8')
                self.ser.write(self.buffer)
                print("Conferma messaggio scritto ",self.message,"|codificato: ",len(self.message)," ",self.buffer)
                print("\n\n")

            else:
                self.set_zero()

    def set_zero(self):
        self.message=str(1100)
        self.buffer=self.message.encode('utf-8')
        while len(self.message)<10:
            self.message=self.message+"."
        self.buffer=self.message.encode('utf-8')
        self.ser.write(self.buffer)    

if __name__ == '__main__':
    comm= CAM()
    comm.start()
