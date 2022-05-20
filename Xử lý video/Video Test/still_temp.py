import cv2
from facenet_pytorch import MTCNN
import numpy as np

class FaceDetector(object):

  def __init__(self,mtcnn):
    self.mtcnn=mtcnn

  def _draw(self,frame,boxes,probs,landmarks):
    for box,prob,ld in zip(boxes,probs,landmarks):
      cv2.rectangle(frame,(box[0],box[1]),(box[2],box[3]),(0,0,255),thickness=2)

      #ve xác suất phát hiện mặt
      cv2.putText(frame,str(prob),(box[2],box[3]),cv2.FONT_HERSHEY_SIMPLEX, 1, (o,0,255),2,cv2.LINE_AA)

      # vẽ các mốc mặt: 2 mắt, mũi, 2 
