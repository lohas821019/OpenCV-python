# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 10:24:32 2022

@author: Jason

想用 Camera 去判斷田間的高低，並也判斷無人車是否走直線

reference:

https://pysource.com/2021/01/28/object-tracking-with-opencv-and-python/
https://its401.com/article/weixin_40247876/117216013
https://www.youtube.com/watch?v=GgGro5IV-cs&ab_channel=Pysource
"""

import cv2
import numpy as np 
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    blank_image = np.zeros((480,640,3), np.uint8)
    cv2.imshow("blank_image", blank_image)
    cv2.imshow("frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()


#%%

# Object detection from Stable camera

cap = cv2.VideoCapture(0)

object_detector = cv2.createBackgroundSubtractorMOG2(history = 100 , varThreshold =40)

while True:
    ret, frame = cap.read()
    # height, width, _ = frame.shape

    # Extract Region of interest
    roi = frame[100: 300,200: 500]

    # 1. Object Detection
    mask = object_detector.apply(frame)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 100:
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
            
    cv2.imshow("mask", mask)
    cv2.imshow("frame", frame)
    cv2.imshow("roi", roi)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()

#%%

import os
os.chdir(r'C:\Users\Jason\Documents\GitHub\OpenCV-python')

from tracker import *

# Object detection from Stable camera

cap = cv2.VideoCapture('./resources/test.mp4')

tracker  = EuclideanDistTracker()

object_detector = cv2.createBackgroundSubtractorMOG2(history = 500 , varThreshold =16)

while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape

    # Extract Region of interest
    roi = frame[100: 300,200: 500]
    
    # roi = frame[400: 1000, 500:1250]


    # 1. Object Detection
    mask = object_detector.apply(frame)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    detections = [] 
    
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 100:
            # cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            
            x, y, w, h = cv2.boundingRect(cnt)
            detections.append([x, y, w, h])
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # 2. Object Tracking
    boxes_ids = tracker.update(detections)
    
    for box_id in boxes_ids:
        x, y, w, h, _id = box_id
        cv2.putText(roi, str(_id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        # cv2.rectangle(roi, (x-w, y-h), (x + w, y + h), (0, 255, 0), 3)

    # print(detections)
    
    cv2.imshow("mask", mask)
    cv2.imshow("frame", frame)
    cv2.imshow("roi", roi)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()

#%%

import cv2

cap = cv2.VideoCapture(0)

while cap.isOpened():
    _, frame = cap.read()
    
    h = frame.shape[0]
    w = frame.shape[1]

    roi = frame[int(h/2):h,0:w]

    cv2.imshow("roi", roi)
    cv2.imshow("roi1", roi)
    cv2.imshow("frame", frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()












