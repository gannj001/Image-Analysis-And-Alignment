# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 11:16:15 2013

@author: John
"""

import cv2

def CannyThreshold(lowThreshold):
    detected_edges = cv2.GaussianBlur(gray,(3,3),0)
    detected_edges = cv2.Canny(detected_edges,lowThreshold,lowThreshold*ratio,apertureSize = kernel_size)
    dst = cv2.bitwise_and(img,img,mask = detected_edges)  # just add some colours to edges from original image.
    cv2.imshow('canny demo',dst)

cap = cv2.VideoCapture('video.avi')

count = 0
while(1):
    _,img = cap.read()
    #img = cv2.blur(img, (3,3))

    cv2.imshow('real image', img)
    
    lowThreshold = 95
    max_lowThreshold = 100
    ratio = 3
    kernel_size = 3
    

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    cv2.namedWindow('canny demo')
    
    #cv2.createTrackbar('Min threshold','canny demo',lowThreshold, max_lowThreshold, CannyThreshold)
    
    CannyThreshold(95)  # initialization
    if cv2.waitKey(33) == 27:
        cv2.destroyAllWindows()
        break
