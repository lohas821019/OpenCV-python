# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 11:56:10 2022

@author: Jason
"""
import os
os.chdir(r'C:\Users\Jason\Documents\GitHub\OpenCV-python')

from predict import *
import cv2

import torch

label = 1
if label == 1:
    global model 
    model = load_model()
    label = 0


cap = cv2.VideoCapture(0)
hw = []

while cap.isOpened():
    _, frame = cap.read()
    
    if hw == []:
        h = frame.shape[0]
        w = frame.shape[1]
        hw.append((h,w))

    roi = frame[int(h/2):h,0:w]
    
    # roi = cv2.imread('./resources/test.png')[:, :, ::-1]
    # roi = roi.copy()
    
    results_roi = model(roi, size=640)  # includes NMS
    results_roi.pred
    data = results_roi.pandas().xyxy[0]    # results_roi = model(roi, size=640)  # includes NMS
    
    
    if not data.empty:

        mid = ((data.xmin + data.xmax)/2,(data.ymin + data.ymax)/2)
    
        point = ((mid[0]-(w/2))**2-(mid[1]-(w/2))**2)**(1/2)
        
        point_loc = point[point == point.min()].index[0]
    
        tangle = data[point_loc:point_loc+1]
        print(tangle)
        
        cv2.rectangle(roi, (int(tangle.xmin), int(tangle.ymin)), (int(tangle.xmax), int(tangle.ymax)), (0, 0, 255), 2)


    cv2.imshow("roi", roi)
    cv2.imshow("frame", frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()


