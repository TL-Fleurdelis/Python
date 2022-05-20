import cv2
import sys
import numpy as np
import math
def distance(point1,point2):
    return np.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
def idealFilterLP(D0,imgShape):
    base = np.zeros(imgShape[:2])
    rows,cols=imgShape[:2]
    center = [rows/2,cols/2]
    for x in range (cols):
        for y in range(rows):
            if distance((y,x),center)<= D0:
                base [y,x] = 1
    return base

def idealFilterHP(D0,imgShape):
    base = np.ones(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows/2,cols/2)
    for x in range(cols):
        for y in range(rows):
            if distance((y,x),center) < D0:
                base[y,x] = 0
    return base

cap = cv2.VideoCapture('temp1.mp4')


while(cap.isOpened()):
    

    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Ideal',frame)
    D0=150
    original = np.fft.fft2(frame)
    center = np.fft.fftshift(original)


    LowPassCenter = center * idealFilterLP(50,frame.shape)
    LowPass = np.fft.ifftshift(LowPassCenter)
    inverse_LowPass = np.fft.ifft2(LowPass)
    
    LowPassCenter2 = center * idealFilterHP(50,frame.shape)
    LowPass2 = np.fft.ifftshift(LowPassCenter2)
    inverse_LowPass2 = np.fft.ifft2(LowPass2)
    
    temp = np.abs(inverse_LowPass)
    temp2= np.abs(inverse_LowPass2)
    cv2.imshow('Ideal low pass filter',temp)
    cv2.imshow('Ideal high pass filter',temp2)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
