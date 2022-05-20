import cv2
import sys
import numpy as np
import math
def distance(point1,point2):
    return np.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
def gaussianLP(D0,imgShape):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows/2,cols/2)
    for x in range(cols):
        for y in range(rows):
            base[y,x] = math.exp(((-distance((y,x),center)**2)/(2*(D0**2))))
    return base

def gaussianHP(D0,imgShape):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows/2,cols/2)
    for x in range(cols):
        for y in range(rows):
            base[y,x] = 1 - math.exp(((-distance((y,x),center)**2)/(2*(D0**2))))
    return base
cap = cv2.VideoCapture('temp1.mp4')


while(cap.isOpened()):
    

    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('My video',frame)
    D0=150
    original = np.fft.fft2(frame)
    center = np.fft.fftshift(original)




    LowPassCenter = center * gaussianLP(50,frame.shape)
    LowPass = np.fft.ifftshift(LowPassCenter)
    inverse_LowPass = np.fft.ifft2(LowPass)




    HighPassCenter = center * gaussianHP(50,frame.shape)
    HighPass = np.fft.ifftshift(HighPassCenter)
    inverse_HighPass = np.fft.ifft2(HighPass)

    
    low= np.abs(inverse_LowPass)
    high= np.abs(inverse_HighPass)
    cv2.imshow('Gaussian low pass filter',low)
    cv2.imshow('Gaussian high pass filter',high)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
