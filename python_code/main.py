from CAM_uart import CAM
from COMM_uart import COMM
#from COMM_receive_uart import READ

#MAIN

#declaration of camera and uarrt comunication
camera = CAM()
comm = COMM()

comm.set_camera(camera)

#start

camera.start()
comm.start()

