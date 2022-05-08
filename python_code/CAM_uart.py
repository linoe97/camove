import cv2
import numpy as np
from threading import Thread

class CAM(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon = True
        self.cam=cv2.VideoCapture(0)   
        self.size=self.get_size_cam()     
        print("Done. Camera Size:",self.size)
        self.initBB=None
        self.right=False
        self.bbox=None

    def run(self):
        vec=[i for i in range(1,8)]
        #advice TLD,MEDIANFLOW,KFC
        while self.right==False:
            self.track_type=int(input("Choose the Tracker by the number:\n   1:BOOSTING\n   2:MIL\n   3:KCF\n   4:TLD\n   5:MEDIANFLOW\n   6:MOSSE\n   7:CSRT\n Input: "))
            if self.track_type in vec:
                self.right=True

        self.tracker=self.choose_track()
        print("Choise Accepted")
        while (self.cam.isOpened()):
            #print("Inizialize camera")
            
            self.key = cv2.waitKey(1) & 0xFF
            self.ret,self.frame= self.cam.read()
            
            cv2.circle(self.frame, (int(self.size[1]/2),int(self.size[0]/2)), radius=0, color=(255, 0, 0), thickness=5) #central point of frame

            if self.initBB is not None:        
                self.ret , self.bbox = self.tracker.update(self.frame)  # bbox=(xmin,ymin,boxwidth,boxheight)
                #print("BOX",self.bbox)
                p1 = (int(self.bbox[0]), int(self.bbox[1]))
                p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
                c = self.center(self.bbox)
                self.actuation(self.bbox)
                cv2.rectangle(self.frame, p1, p2, (0,255,0), 2, 1)  #object tracked
                cv2.circle(self.frame, c, radius=0, color=(0, 0, 255), thickness=5) #center of the object
            else:
                self.ret = None 
                self.bbox = None
                
            if self.key==ord('s'):
                self.initBB = None
                self.bbox = None
                self.initBB=cv2.selectROI("CAMERA", self.frame, fromCenter=False,
                    showCrosshair=True) #set the inital box to track
                self.tracker.init(self.frame, self.initBB) 
                print("Start Tracking")


            cv2.imshow("CAMERA",self.frame)

            if self.key==ord('q'):
                break   

                   
        self.cam.release()
        cv2.destroyAllWindows()        
                
    #scelgo il tracker
    def choose_track(self,):                        
        if self.track_type==1:
            return cv2.TrackerBoosting_create()
        elif self.track_type==2:
            return cv2.TrackerMIL_create()
        elif self.track_type==3:
            return cv2.TrackerKCF_create()
        elif self.track_type==4:
            return cv2.TrackerTLD_create()
        elif self.track_type==5:
            return cv2.TrackerMedianFlow_create()
        elif self.track_type==6:
            return cv2.TrackerMOSSE_create()
        elif self.track_type==7:
            return cv2.TrackerCSRT_create()

    def actuation(self,box):                            
        c = self.center(box)
        if c[0]==int(self.size[1]/2):
            if c[1]==int(self.size[0]/2):
                cv2.putText(self.frame,"CENTER",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            elif c[1]<int(self.size[0]/2):
                cv2.putText(self.frame,"NORD",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            elif c[1]>int(self.size[0]/2):
                cv2.putText(self.frame,"SOUTH",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
    
        elif c[0]<int(self.size[1]/2):
            if c[1]==int(self.size[0]/2):
                cv2.putText(self.frame,"WEST",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            elif c[1]<int(self.size[0]/2):
                cv2.putText(self.frame,"NW",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            elif c[1]>int(self.size[0]/2):
                cv2.putText(self.frame,"SW",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        elif c[0]>int(self.size[1]/2):
            if c[1]==int(self.size[0]/2):
                cv2.putText(self.frame,"EST",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            elif c[1]<int(self.size[0]/2):
                cv2.putText(self.frame,"NE",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            elif c[1]>int(self.size[0]/2):
                cv2.putText(self.frame,"SE",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    #Individuo le dimensioni del frame. Get resolution of the frame
    def get_size_cam (self):                              
        height=self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width=self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        info_dim=[height,width]
        return info_dim

    #indivuo il centro del frame. Find the frame center
    def center(self,box):                                 
        x=int(box[0] + box[2]/2)
        y=int(box[1] + box[3]/2)
        return (x,y)

#N.B. center(x,y),size(y,x)
    def deviation(self):
        c=self.center(self.bbox)
        if c[0]>self.size[1]/2:
            x=c[0]-self.size[1]/2
        else:
            x=-(self.size[1]/2-c[0])

        if c[1]>self.size[0]/2:
            y=c[1]-self.size[0]/2
        else:
            y=-(self.size[0]/2-c[1])
        return (int(x),int(y))

if __name__ == '__main__':
    camera= CAM()
    camera.start()