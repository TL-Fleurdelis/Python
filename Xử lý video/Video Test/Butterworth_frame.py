import cv2
import sys
import numpy as np
import math
def distance(point1,point2):
    return np.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
def butterworthLP(D0,imgShape,n):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows/2,cols/2)
    for x in range(cols):
        for y in range(rows):
            base[y,x] = 1/(1+(distance((y,x),center)/D0)**(2*n))
    return base

def butterworthHP(D0,imgShape,n):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows/2,cols/2)
    for x in range(cols):
        for y in range(rows):
            base[y,x] = 1-1/(1+(distance((y,x),center)/D0)**(2*n))
    return base
cap = cv2.VideoCapture('temp1.mp4')


while(cap.isOpened()):
    

    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('My video',frame)
    D0=150
    original = np.fft.fft2(frame)
    center = np.fft.fftshift(original)


    LowPassCenter = center * butterworthLP(50,frame.shape,10)
    LowPass = np.fft.ifftshift(LowPassCenter)
    inverse_LowPass = np.fft.ifft2(LowPass)
    
    HighPassCenter = center * butterworthHP(50,frame.shape,10)
    HighPass = np.fft.ifftshift(HighPassCenter)
    inverse_HighPass = np.fft.ifft2(HighPass)
    #plt.subplot(132), plt.imshow(np.abs(inverse_HighPass), "gray"), plt.title("Butterworth High Pass (n=10)")
    
    low = np.abs(inverse_LowPass)
    high= np.abs(inverse_HighPass)
    cv2.imshow('butterworth low pass filter',low)
    cv2.imshow('butterworth high pass filter',high)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
