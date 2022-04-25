# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 11:56:10 2022

@author: Jason
"""

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


