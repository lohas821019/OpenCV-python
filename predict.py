# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 13:59:31 2022

@author: Jason

https://stackoverflow.com/questions/70167811/how-to-load-custom-model-in-pytorch

    '''
    #model.eval()的作用是不启用 Batch Normalization 和 Dropout。
    训练完train样本后，生成的模型model要用来测试样本。
    在model(test)之前，需要加上model.eval()，否则的话，有输入数据，
    即使不训练，它也会改变权值。这是model中含有BN层和Dropout所带来的的性质。
    '''
    
    '''
    with torch.no_grad()则主要是用于停止autograd模块的工作，
    以起到加速和节省显存的作用。
    它的作用是将该with语句包裹起来的部分停止梯度的更新，
    从而节省了GPU算力和显存，但是并不会影响dropout和BN层的行为。
    '''

"""
import os
import cv2
import torch
from PIL import Image

def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt', force_reload=True) 
    model.eval()
    
    return model

# global model 
# model = load_model()

def pred_img(img,model):
    
    with torch.no_grad():
        
        # Images
        img = cv2.imread(img_path)[:, :, ::-1]  # OpenCV image (BGR to RGB)
        # Inference
        results = model(img, size=640)  # includes NMS
        # results.display()
        # results.show()
    
        # results.print()  
        # results.save()  # or .show()
        
        results.xyxy[0]  # img1 predictions (tensor)
        results.pandas().xyxy[0] #取得圈出的框框 以及confidence
        
        
    
    

