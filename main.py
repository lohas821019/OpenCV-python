# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 11:56:10 2022

@author: Jason
"""
import os
os.chdir(r'C:\Users\Jason\Documents\GitHub\OpenCV-python')


#使用一般webcam
from predict import *
import cv2
import torch
import time

label = 1
if label == 1:
    global model 
    model = load_model()
    label = 0

#%%
path =r'C:\Users\Jason\Desktop\20220416\IMG_9073.MOV'
cap = cv2.VideoCapture(path)

# cap = cv2.VideoCapture(1)

hw = []

while cap.isOpened():
    _, frame = cap.read()
    
    if hw == []:
        
        h = frame.shape[0]
        w = frame.shape[1]
        hw.append((h,w))
        region = []

    roi = frame[int(h/2):h,0:w]
    
    # cv2.imwrite('./resources/test1.png', frame)
    # time.sleep(0.3)
    # roi = cv2.imread('./resources/test1.png')[:, :, ::-1]
    
    results_roi = model(roi, size=640)  # includes NMS
    results_roi.pred
    data = results_roi.pandas().xyxy[0]    # includes NMS
    # time.sleep(0.3)
    # print(len(data))
    
    try:
        for i in range(0,len(data)):
            data = data.iloc[i]
            #xmin,ymin,xmax,ymax
            region = [int(data.xmin), int(data.ymin), int(data.xmax), int(data.ymax)]
            cv2.rectangle(roi, (int(data.xmin), int(data.ymin)), (int(data.xmax), int(data.ymax)), (0, 0, 255), 2)
            mid = ((data.xmin + data.xmax)/2,(data.ymin + data.ymax)/2)
            print(mid)
            cv2.circle(roi,(int(mid[0]),int(mid[1])), 15, (0, 0, 255), -1)
    except:
        pass
    # if not data.empty:

    #     mid = ((data.xmin + data.xmax)/2,(data.ymin + data.ymax)/2)
    
    #     point = ((mid[0]-(w/2))**2-(mid[1]-(h/4))**2)**(1/2)
        
    #     point_loc = point[point == point.min()].index[0]
    
    #     tangle = data[point_loc:point_loc+1]
    #     print(tangle)
        
    #     cv2.rectangle(roi, (int(tangle.xmin), int(tangle.ymin)), (int(tangle.xmax), int(tangle.ymax)), (0, 0, 255), 2)

    cv2.imshow("roi", roi)
    # cv2.imshow("frame", frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()


#%%
#使用深度相機
from predict import *
import cv2
import torch
import numpy as np
import pyrealsense2 as rs

#深度相機
# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False

for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

hw = []

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data()) 
        
        if hw == []:
            h = depth_frame.height
            w = depth_frame.width
            hw.append((h,w))
        roi = color_image[int(h/2):h,0:w]
        
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        with torch.no_grad():
            results_roi = model(color_image, size=640)  # includes NMS
            results_roi.pred
            data = results_roi.pandas().xyxy[0]  # includes NMS
            # print(data)
            
            try:
                for i in range(0,len(data)):
                    data = data.iloc[i]
                    cv2.rectangle(color_image, (int(data.xmin), int(data.ymin)), (int(data.xmax), int(data.ymax)), (0, 0, 255), 2)
                    cv2.rectangle(roi, (int(data.xmin), int(data.ymin)), (int(data.xmax), int(data.ymax)), (0, 0, 255), 2)
                    mid = ((data.xmin + data.xmax)/2,(data.ymin + data.ymax)/2)
                    print(mid)
                    
                    print(f"depth_frame.get_distance() = {depth_frame.get_distance(int(mid[0]),int(mid[1]))}")
                    
                    cv2.circle(color_image,(int(mid[0]),int(mid[1])), 10, (0, 0, 255), -1)
                    cv2.circle(roi,(int(mid[0]),int(mid[1])), 10, (0, 0, 255), -1)
            except:
                pass
            
        # If depth and color resolutions are different, resize color image to match depth image for display
        # if depth_colormap_dim != color_colormap_dim:
        #     resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
        #     images = np.hstack((resized_color_image, depth_colormap))
        # else:
        #     images = np.hstack((color_image, depth_colormap))

        # Show images
        # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)

            cv2.imshow('RealSense', color_image)
            cv2.imshow('RealSense_depth', depth_colormap)
            cv2.imshow('roi',roi)
            
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break

finally:

    # Stop streaming
    cv2.destroyAllWindows()
    pipeline.stop()
        

"""
2022/04/26紀錄
測試時使用，
若使用Camera 直接拍攝螢幕展示的影片會無法判斷出來任何雜草，
放大以後效果也是依樣，但如果把影像單獨輸入進去，卻可以判斷。

"""


