#THIS CODE WORK WITH COMM_DMA (stm32CubeMX)

import serial 

ser = serial.Serial('COM7',baudrate=115200)  # open serial port
i=0
while(1):
    print("ciclo",i)
    reading = ser.readline() #read a string
    print("Lettura",reading)
    #print(ser.name)         # check which port was really used
    if i==5:
        ser.write(b'hello')     # write a string
        reading = ser.readline()
        print("Lettura send",reading)
        i=0
    i+=1
    
    #ser.close()  
    