# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 10:54:36 2022

@author: Jason
"""

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    #Sobel
    x = cv2.Sobel(frame,cv2.CV_16S,1,0)
    y = cv2.Sobel(frame,cv2.CV_16S,0,1)
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)
    dst = cv2.addWeighted(absX,0.5,absY,0.5,0.5)
    
    #轉為灰階
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #使用閥值
    _, mask = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    #使用Canny
    thresh = cv2.Canny(gray, 128, 256)

    #隨著使用方式修改要顯示的輪廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 10:
            cv2.drawContours(thresh, [cnt], -1, (0, 255, 0), 2)


    cv2.imshow("thresh", thresh)
    cv2.imshow("mask", mask)
    cv2.imshow("frame", frame)
    cv2.imshow("dst", dst)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()