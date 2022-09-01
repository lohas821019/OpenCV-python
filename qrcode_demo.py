# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 14:56:35 2022

@author: Jason
"""

import cv2

img = cv2.imread('qr1.jpg')
qr_detector = cv2.QRCodeDetector()
retval, points, straight_qrcode = qr_detector.detectAndDecode(img)
print('text=' + retval)

#%%
import cv2

cap = cv2.VideoCapture(0)
qr_detector = cv2.QRCodeDetector()

while True:
    _, frame = cap.read()
    retval, points, straight_qrcode = qr_detector.detectAndDecode(frame)
    
    print(f'retval = {retval}')
    print(f'points = {points}')
    print(f'straight_qrcode = {straight_qrcode}')
    
    cv2.imshow("frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()

#%%
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol 
import pyzbar

import cv2


cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray)
    print(barcodes)
    
    # for barcode in barcodes:
    #     print(barcode)
    #     (x, y, w, h) = barcode.rect
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #     cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 0, 255), 2)
     
    #     barcodeData = barcode.data.decode("utf-8")
    #     barcodeType = barcode.type
     
    #     text = "{} ({})".format(barcodeData, barcodeType)
    #     cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,.5, (0, 0, 125), 2)
    #     cv2.putText(gray, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,.5, (0, 0, 125), 2)
        
    cv2.moveWindow("QRcode掃描",200,35)
    cv2.waitKey(20)

    cv2.imshow("frame", frame)
    cv2.imshow("gray", gray)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()

#%%

from pyzbar.pyzbar import decode
import cv2
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

cap.set(3,640)
cap.set(4,480)

while True:
    _, frame = cap.read()
    for barcode in decode(frame):
        mydata = barcode.data.decode('utf-8')
        print(mydata)
        pts = np.array([barcode.polygon],np.int32)
        cv2.polylines(frame,[pts],True,(255,0,255),5)
        pts2 = barcode.rect
        cv2.putText(frame, mydata, (pts2[0],pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,0.9, (255, 0, 255), 2)

    cv2.imshow("frame", frame)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()

#%%

def detect_QRCode():
    from pyzbar.pyzbar import decode
    import cv2
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap.set(3,640)
    cap.set(4,480)

    while True:
        _, frame = cap.read()
        for barcode in decode(frame):
            mydata = barcode.data.decode('utf-8')
            print(mydata)
            pts = np.array([barcode.polygon],np.int32)
            cv2.polylines(frame,[pts],True,(255,0,255),5)
            pts2 = barcode.rect
            cv2.putText(frame, mydata, (pts2[0],pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,0.9, (255, 0, 255), 2)
        cv2.imshow("frame", frame)
        
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()


#%%
qrcode_flag = 0
def detect_QRCode(qrcode_flag):
    from pyzbar.pyzbar import decode
    import cv2
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()
        cv2.imshow("frame", frame)
        k = cv2.waitKey(1) & 0xFF
        
        if k == 27:
            break

        for barcode in decode(frame):
            mydata = barcode.data.decode('utf-8')
            print(mydata)

            pts = np.array([barcode.polygon],np.int32)
            cv2.polylines(frame,[pts],True,(255,0,255),5)
            pts2 = barcode.rect
            cv2.putText(frame, mydata, (pts2[0],pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,0.9, (255, 0, 255), 2)

            if len(mydata)>5:
                qrcode_flag = 1

        if qrcode_flag:
            break


    cv2.destroyAllWindows()
    cap.release()
    
    #%%
    
while True:

    rfid_flag = 1
    print(1)
    if rfid_flag:
        rfid_flag = 0
        break
    

qrcode_flag = 1
print('qrcode_flag= '+ str(qrcode_flag))

print(f'{qrcode_flag}=qrcode_flag123')








