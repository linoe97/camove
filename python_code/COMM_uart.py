import serial 
from CAM_uart import CAM
from threading import Thread

class COMM(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon = True
        #INSERIRE PORTA COM GIUSTA
        #self.ser= serial.Serial('COM7',baudrate=115200)
        self.ser= serial.Serial('COM5',baudrate=115200)
        self.dev=(0,0)
        self.message=None
        self.buffer=None
        self.reading=None

    def set_camera(self,cam):
        self.camera=cam

    def run(self):
        while self.camera.cam.isOpened(): 
            if self.camera.bbox is not None:
                self.dev=self.camera.deviation()
                print("Deviation X: ",self.dev[0]," Y: ",self.dev[1])
                print("lenght X: ",len(str(self.dev[0]))," lenght Y: ",len(str(self.dev[1])))
                self.message=str(len(str(self.dev[0])))+str(len(str(self.dev[1])))+str(self.dev[0])+str(self.dev[1])
                print("Messaggio: ",self.message)
                while len(self.message)<10:
                    self.message=self.message+"."
                self.buffer=self.message.encode('utf-8')
                self.ser.write(self.buffer)
                print("Conferma messaggio scritto ",self.message,". ",len(self.message)," ",self.buffer)
                #self.reading = self.ser.read(len(str(self.dev[0])))
                #if self.reading==None:
                #    pass
                #else: 
                #    print("Lettura porta uart",self.reading,".")
                print("\n\n")
            #if self.ser.readlines()!=None:
            #    self.reading = self.ser.readline()
            #    print("Lettura porta uart",self.reading,".\n")

if __name__ == '__main__':
    comm= CAM()
    comm.start()
