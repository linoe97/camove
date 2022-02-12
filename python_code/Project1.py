import numpy as np 
import cv2

#Individuo le dimensioni del frame
def get_size_cam (frame):                              
    height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    info_dim=[height,width]
    return info_dim

#indivuo il centro del frame
def center(box,size):                                 
    x=int(bbox[0] + bbox[2]/2)
    y=int(bbox[1] + bbox[3]/2)
    return (x,y)

#mostro a schermo la posizione in termini cardinali del soggetto rispetto al centro del frame
def actuation(box,size,vid):                            
    c = center(box,size)
    if c[0]==int(size[1]/2):
        if c[1]==int(size[0]/2):
            cv2.putText(vid,"CENTRO",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        elif c[1]<int(size[0]/2):
            cv2.putText(vid,"NORD",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        elif c[1]>int(size[0]/2):
            cv2.putText(vid,"SUD",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
  
    elif c[0]<int(size[1]/2):
        if c[1]==int(size[0]/2):
            cv2.putText(vid,"WEST",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        elif c[1]<int(size[0]/2):
            cv2.putText(vid,"NW",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        elif c[1]>int(size[0]/2):
            cv2.putText(vid,"SW",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    elif c[0]>int(size[1]/2):
        if c[1]==int(size[0]/2):
            cv2.putText(vid,"EST",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        elif c[1]<int(size[0]/2):
            cv2.putText(vid,"NE",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        elif c[1]>int(size[0]/2):
            cv2.putText(vid,"SE",(100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

#scelgo il tracker
def choose_track(track):                        
    if track==1:
        return cv2.TrackerBoosting_create()
    elif track==2:
        return cv2.TrackerMIL_create()
    elif track==3:
        return cv2.TrackerKCF_create()
    elif track==4:
        return cv2.TrackerTLD_create()
    elif track==5:
        return cv2.TrackerMedianFlow_create()
    elif track==6:
        return cv2.TrackerMOSSE_create()
    elif track==7:
        return cv2.TrackerCSRT_create()


#MAIN
cap=cv2.VideoCapture(0)
initBB=None
right=False

vec=[i for i in range(1,8)]

#consigliati TLD,MEDIANFLOW,KFC
while right==False:
    track_type=int(input("Choose the Tracker:\n   1:BOOSTING\n   2:MIL\n   3:KCF\n   4:TLD\n   5:MEDIANFLOW\n   6:MOSSE\n   7:CSRT\n Input: "))
    if track_type in vec:
        right=True

tracker=choose_track(track_type)

if cap.isOpened==False:
    print("Accesso alla videocamera fallito")
else:
    size=get_size_cam(cap)

while (cap.isOpened()):
    #print("Inizialize camera")
    
    key = cv2.waitKey(1) & 0xFF
    ret,frame= cap.read()
    

    if initBB is not None:        
        ret , bbox = tracker.update(frame)
        #print("BOX",bbox)
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        c = center(bbox,size)
        actuation(bbox,size,frame)
        cv2.rectangle(frame, p1, p2, (0,255,0), 2, 1)
        cv2.circle(frame, c, radius=0, color=(0, 0, 255), thickness=5)

    if key==ord('s'):
        initBB=cv2.selectROI("CAMERA", frame, fromCenter=False,
			showCrosshair=True)
        tracker.init(frame, initBB)
        print("Track Iniziato")

    cv2.imshow("CAMERA",frame)

    if key==ord('q'):
        break   


cap.release()
cv2.destroyAllWindows()        