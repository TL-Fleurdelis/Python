'''
Author: Trương Thành Long
Mã sinh viên:78879
Lớp:CNT59ĐH
Đề tài: Xây dựng một chương trình xử lý ảnh cho phép đọc file video, xử lý từng 
frame và hiển thị kết quả nhận được, các phép xử lý sau:

+ Các thao tác xử lý dựa trên điểm ảnh (cân bằng histogram, tách ngưỡng, lấy 
âm bản, biến đổi lograrith, tăng độ tương phản).

+ Các phép lọc không gian (mean, median, Gaussian, linear sharpen, lấy ảnh 
gradient, edge detection).

+ Các phép lọc ảnh trong miền tần số (lọc thông thấp và lọc thông cao).

+ Thực hiện lọc ảnh bằng bộ lọc Bilateral và NonLocalMeans.
'''

from tkinter import *
from tkinter import messagebox
import numpy as np
import cv2
from tkinter import filedialog
import math
import sys
from PIL import ImageTk,Image

#Link video
def browseFiles():

    global data
    data = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.mp4*"),
                                                       ("all files",
                                                        "*.*")))
      
    # Change label contents
    label_filename.configure(text="Link: "+data)
    
# -----------------------------Video Processing---------------------------------
def Exit():
    answer=messagebox.askquestion("Thông báo","Bạn muốn thoát ?")
    if answer =="yes":
        wd.destroy()
#Edge detection
def edge():

    cap = cv2.VideoCapture(data)
    while(cap.isOpened()):
    

        ret, frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        #Edge dectection
        edges = cv2.Canny(frame,100,200)
        cv2.imshow('Edge detection',edges)
    

 
        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
#Gaussian Blur
def gauss_blur():
    cap = cv2.VideoCapture(data)
    while(cap.isOpened()):
    

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    


        #cv2.imshow('Gray video',gray)
        #cv2.imshow('My video',frame)
        im_gaussian = cv2.GaussianBlur(gray,(5,5),0)
        cv2.imshow("Gaussian filter video", im_gaussian)
 
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
#Gradient
def gradient():
    cap = cv2.VideoCapture(data)
    while(cap.isOpened()):
    

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        laplacian = cv2.Laplacian(frame, cv2.CV_64F)
        sobelx = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize=3)
        sobelxy = cv2.Sobel(frame, cv2.CV_64F, 1, 1, ksize=3)
        #print('[Before Scale] laplacian image min-max:', np.min(laplacian), '-', np.max(laplacian))
    
        #gradient
        cv2.imshow('before_scale-laplacian', laplacian)
        cv2.imshow('before_scale-sobelx', sobelx)
        cv2.imshow('before_scale-sobely', sobely)
        cv2.imshow('before_scale-sobelxy', sobelxy)
    
        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
#Linear Sharpen
    
def linear_sharpen():
    cap = cv2.VideoCapture(data)
    while(cap.isOpened()):
    

        ret, frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        #linear sharpen
    
        #sharpen_filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        #sharped_img = cv2.filter2D(frame, -1, sharpen_filter)
        #cv2.imshow('Linear sharpen',sharped_img )
    
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpen= cv2.filter2D(frame, -1, kernel)
        cv2.imshow('Linear sharpen',sharpen )
 
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
#Mean filter
    
def mean ():
    cap = cv2.VideoCapture(data)
    while(cap.isOpened()):
        
        ret, frame = cap.read()
    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Mean/Box
        im_meanblur = cv2.blur(frame,(5,5))
        cv2.imshow("Mean/Box filter image", im_meanblur)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
#Median filter
    
def median ():
    cap = cv2.VideoCapture(data)
    while(cap.isOpened()):
    
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
        im_median = cv2.medianBlur(frame,5)
        cv2.imshow("Median filter video", im_median)


 
        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
#My video
    
def video():
    cap = cv2.VideoCapture(data)
    
    while(cap.isOpened()):
    

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        #blur = cv2.medianBlur(frame,5)


        cv2.imshow('Gray video',gray)
        cv2.imshow('My video',frame)



 
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
#Equal Hist
    
def hist():
    cap = cv2.VideoCapture(data)
    #Hàm tính toán histogram

    while(cap.isOpened()):
    

        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dst = cv2.equalizeHist(frame)
        cv2.imshow("Original",frame)
        cv2.imshow("Equal Hist",dst)
    
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    
#Threshold(Tách ngưỡng)
    
def Threshold():
    cap = cv2.VideoCapture(data)


    while(cap.isOpened()):
    

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.medianBlur(frame,5)
        
        #Simple Thresholding 
        _,th1 = cv2.threshold(frame, 50, 255, cv2.THRESH_BINARY)
        _,th2 = cv2.threshold(frame, 50, 255, cv2.THRESH_BINARY_INV)
        _,th3 = cv2.threshold(frame, 50, 255, cv2.THRESH_TRUNC)
        _,th4 = cv2.threshold(frame, 50, 255, cv2.THRESH_TOZERO)

    
        #Aldaptive Thresholding 
        #ret,th1 = cv2.threshold(frame,50,255,cv2.THRESH_BINARY)
        #th2 = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
        #th3 = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        cv2.imshow('My video',frame)
        cv2.imshow('THRESH_BINARY',th1)
        cv2.imshow('THRESH_BINARY_INV',th2)
        cv2.imshow('THRESH_TRUNC',th3)
        cv2.imshow('THRESH_TOZERO',th4)


    
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
#Negative - Âm bản
    
def negative():
    cap = cv2.VideoCapture(data)

    while(cap.isOpened()):
    

        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #frame_neg=255-frame
        frame_neg = cv2.bitwise_not(frame)
        cv2.imshow('My video',frame)
        cv2.imshow('Negative video',frame_neg)
    
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()

    cv2.destroyAllWindows()
    
#Contrast- Tương phản
    
def contrast():
    cap = cv2.VideoCapture(data)


    while(cap.isOpened()):
    
        ret, frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  
        alpha = 2
        beta = 50
    
        result = cv2.addWeighted(frame, alpha, np.zeros(frame.shape, frame.dtype),0,beta)
    
        cv2.imshow('Original',frame)
        cv2.imshow('Constrast',result)
    
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
#Logarithm
def log():
    cap = cv2.VideoCapture(data)


    while(cap.isOpened()):
    

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        c = 255 / np.log(1 + np.max(gray))
        log_frame = c*(np.log(gray + 1))
        log_frame = np.array(log_frame, dtype = np.uint8)
        cv2.imshow("My video",frame)
        cv2.imshow("Log frame",log_frame)
    
        if cv2.waitKey(300) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
#Bilateral
    
def bilateral():
    cap = cv2.VideoCapture(data)


    while(cap.isOpened()):
    

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bilateral = cv2.bilateralFilter(frame, 15, 75, 75)

        cv2.imshow("My video",frame)
        cv2.imshow("Bilateral",bilateral)
    
        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#Non local means
    
def non_local_means():
    cap = cv2.VideoCapture(data)
    while(cap.isOpened()):
    

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # create a list of first 5 frames
        frame = [cap.read()[1] for i in range(20)]
        # convert all to grayscale
        gray = [cv2.cvtColor(i, cv2.COLOR_BGR2GRAY) for i in frame]
        # convert all to float64
        gray = [np.float64(i) for i in gray]
        # create a noise of variance 25
        noise = np.random.randn(*gray[1].shape)*10
        # Add this noise to images
        noisy = [i+noise for i in gray]
        # Convert back to uint8
        noisy = [np.uint8(np.clip(i,0,255)) for i in noisy]
        # Denoise 3rd frame considering all the 5 frames
        dst = cv2.fastNlMeansDenoisingMulti(noisy, 2, 5, None, 4, 7, 35)
    
        #dst = cv2.fastNlMeansDenoisingColored(frame,None,10,10,7,21)
        #cv2.imshow('Non local means (gray)',gray[2])
        #cv2.imshow('Non local means (noisy)',noisy[2])
        cv2.imshow('Non local means dst',dst)

    
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
def distance(point1,point2):
    return np.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
#High pass filters
def idealFilterHP(D0,imgShape):
    base = np.zeros(imgShape[:2])
    rows,cols=imgShape[:2]
    center = [rows/2,cols/2]
    for x in range (cols):
        for y in range(rows):
            if distance((y,x),center)>= D0:
                base [y,x] = 1
    return base
def butterworthHP(D0,imgShape,n):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows/2,cols/2)
    for x in range(cols):
        for y in range(rows):
            base[y,x] = 1-1/(1+(distance((y,x),center)/D0)**(2*n))
    return base
def gaussianHP(D0,imgShape):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows/2,cols/2)
    for x in range(cols):
        for y in range(rows):
            base[y,x] = 1 - math.exp(((-distance((y,x),center)**2)/(2*(D0**2))))
    return base

#Low pass filters
def idealFilterLP(D0,imgShape):
    base = np.zeros(imgShape[:2])
    rows,cols=imgShape[:2]
    center = [rows/2,cols/2]
    for x in range (cols):
        for y in range(rows):
            if distance((y,x),center)<= D0:
                base [y,x] = 1
    return base

def butterworthLP(D0,imgShape,n):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows/2,cols/2)
    for x in range(cols):
        for y in range(rows):
            base[y,x] = 1/(1+(distance((y,x),center)/D0)**(2*n))
    return base

def gaussianLP(D0,imgShape):
    base = np.zeros(imgShape[:2])
    rows, cols = imgShape[:2]
    center = (rows/2,cols/2)
    for x in range(cols):
        for y in range(rows):
            base[y,x] = math.exp(((-distance((y,x),center)**2)/(2*(D0**2))))
    return base

# Output High pass filters
def high_pass_filters():
    cap = cv2.VideoCapture(data)

    while(cap.isOpened()):
    

        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        D0=150
        ideal = idealFilterHP(D0,frame.shape)
        butterworth = butterworthHP (D0,frame.shape,5)
        gaussian = gaussianHP(D0,frame.shape)
        cv2.imshow("Ideal high pass filter",ideal)
        cv2.imshow("Butterworth high pass filter",butterworth)
        cv2.imshow("Gaussian high pass filter",gaussian)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
# Output Low pass filters    
def low_pass_filters():
    cap = cv2.VideoCapture(data)


    while(cap.isOpened()):
    

        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        D0=150
        ideal = idealFilterLP(D0,frame.shape)
        butterworth = butterworthLP (D0,frame.shape,5)
        gaussian = gaussianLP(D0,frame.shape)
        cv2.imshow("Ideal low pass filter",ideal)
        cv2.imshow("Butterworth low pass filter",butterworth)
        cv2.imshow("Gaussian low pass filter",gaussian)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#Window
wd=Tk()
wd.geometry("800x800")
wd.title("Project 2")

#wd.configure(bg='black')

#Background image

img = ImageTk.PhotoImage(Image.open("background.jpg"))
panel = Label(wd, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")

#Create buttons and labels
label_filename = Label(wd,font="Time 10 bold",
                            text = "Video Processing Python",
                           
                            fg = "pink")
       
bt_file = Button(wd,font="Time 9 bold",fg='Cyan',bg='Purple',
                        text = "Browse Files",
                        command = browseFiles)
label_filename.place(x=310,y=0)
bt_file.place(x=350,y=50)

  
Exit=Button(wd,text='Exit',font="Time 9 bold",command=Exit,fg='Blue',bg='Yellow')
Exit.place(x=5,y=300,width=90)

bt_video=Button(wd,text='My Video',font="Time 9 bold",command=video,fg='Blue',bg='Yellow')
bt_video.place(x=5,y=100,width=90)

bt_mean=Button(wd,text='Mean filters',font="Time 9 bold",command=mean,fg='Blue',bg='Yellow')
bt_mean.place(x=100,y=100,width=90)

bt_mean=Button(wd,text='Median filters',font="Time 9 bold",command=median,fg='Blue',bg='Yellow')
bt_mean.place(x=195,y=100,width=90)

bt_mean=Button(wd,text='Gaussian filters',font="Time 9 bold",command=gauss_blur,fg='Blue',bg='Yellow')
bt_mean.place(x=290,y=100,width=90)

bt_sharp=Button(wd,text='Linear Sharpen',font="Time 9 bold",command=linear_sharpen,fg='Blue',bg='Yellow')
bt_sharp.place(x=385,y=100,width=90)

bt_gra=Button(wd,text='Gradient ',font="Time 9 bold",command=gradient,fg='Blue',bg='Yellow')
bt_gra.place(x=480,y=100,width=100)

bt_edge=Button(wd,text='Edge detection',font="Time 9 bold",command=edge,fg='Blue',bg='Yellow')
bt_edge.place(x=590,y=100,width=100)

bt_hist=Button(wd,text='Equal Hist',font="Time 9 bold",command=hist,fg='Blue',bg='Yellow')
bt_hist.place(x=5,y=150,width=90)

bt_TN=Button(wd,text='Threshold',font="Time 9 bold",command=Threshold,fg='Blue',bg='Yellow')
bt_TN.place(x=100,y=150,width=90)

bt_neg=Button(wd,text='Negative',font="Time 9 bold",command=negative,fg='Blue',bg='Yellow')
bt_neg.place(x=195,y=150,width=90)

bt_con=Button(wd,text='High Contrast',font="Time 9 bold",command=contrast,fg='Blue',bg='Yellow')
bt_con.place(x=290,y=150,width=90)

bt_log=Button(wd,text='Logarithm',font="Time 9 bold",command=log,fg='Blue',bg='Yellow')
bt_log.place(x=385,y=150,width=90)

bt_non=Button(wd,text='Non local means',font="Time 9 bold",command=non_local_means,fg='Blue',bg='Yellow')
bt_non.place(x=480,y=150,width=100)

bt_bil=Button(wd,text='Bilateral',font="Time 9 bold",command=bilateral,fg='Blue',bg='Yellow')
bt_bil.place(x=590,y=150,width=100)

bt_high_pass=Button(wd,text='High pass filters',font="Time 9 bold",command=high_pass_filters,fg='Blue',bg='Yellow')
bt_high_pass.place(x=5,y=200,width=100)

bt_low_pass=Button(wd,text='Low pass filters',font="Time 9 bold",command=low_pass_filters,fg='Blue',bg='Yellow')
bt_low_pass.place(x=120,y=200,width=100)
