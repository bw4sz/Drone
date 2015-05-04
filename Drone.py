#!/usr/bin/env python

import cv2
import numpy as np
import time
import os
import sfunc
          
###Create photo class with sensible defaults

class photo:

        def __init__(self,f):                  
                print("Photo Object")
                self.img=cv2.imread(f)
                sfunc.cView(self.img)                
                
        def quadrat(self):

                #Detect red flagging
                
                #Turn to HSV color space
                img_hsv=cv2.cvtColor(self.img,cv2.COLOR_BGR2HSV)
                sfunc.cView(img_hsv)
                
                #threshold colors
                
                #what is a flag color? Its somewhere between white and red
                # i googled these colors
                RED_MIN = np.array([160, 120, 120],np.uint8)
                RED_MAX = np.array([180, 255, 255],np.uint8)
                
                frame_threshed = cv2.inRange(src=img_hsv, lowerb=RED_MIN, upperb=RED_MAX)
                sfunc.cView(frame_threshed)
                
                #inflate sections to remove any small blips
                kernel = np.ones((100,100),np.uint8)
                closing = cv2.dilate(frame_threshed, kernel,2)
                sfunc.cView(closing)
                
                #draw contours 
                image, contours, hierarchy = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                
                #find the largest contour
                area = []
                for cnt in contours:
                    area.append(cv2.contourArea(cnt))
                
                #find largest contour
                themax=area.index(max(area))
                
                #make a mask out of that area
                mask = np.zeros(image.shape[:2], np.uint8)
                mask=cv2.drawContours(mask, contours[themax], -1, 255, 1)
                sfunc.cView(mask)
                
                # Perform morphology
                se = np.ones((200,200), dtype='uint8')
                image_close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, se)
                sfunc.cView(image_close)
                
                ##refind contours
                #make a mask out of that area
                image, contours, hierarchy = cv2.findContours(image_close,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
                
                #define new mask
                mask2 = np.zeros(image.shape[:2], np.uint8)
                
                #find area
                area = []
                for cnt in contours:
                    area.append(cv2.contourArea(cnt))    
                
                #small contour that capture the shape?
                #this needs to be thought about, i think want the inner not the outer contour.
                themin=area.index(min(area))
                
                #Draw plot
                mask2 = cv2.drawContours(mask2, contours, themin, (255,255,255), thickness=-1)
                sfunc.cView(mask2)
                
                #mask original frame by quadrat plot
                self.img_crop=cv2.bitwise_and(self.img,self.img,mask=mask2)
                sfunc.cView(self.img_crop)
        def count(self):
                ###Cluster images
                #threshold colors
                
                ##what is a flower color? Its somewhere between white and red
                ## i googled these colors
                WHITE_MIN = np.array([220, 220, 220],np.uint8)
                WHITE_MAX = np.array([255, 255, 255],np.uint8)
                
                frame_threshed = cv2.inRange(src=img_crop, lowerb=WHITE_MIN, upperb=WHITE_MAX)
                sfunc.cView(frame_threshed)
                
                #view segmented imaged
                cropthresh=cv2.bitwise_and(img_crop,img_crop,mask=frame_threshed)
                sfunc.cView(cropthresh)
                
                # count number of clusters
                image, contours, hierarchy = cv2.findContours(frame_threshed,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                
                #draw clusters on a copy of the original image 
                cropcopy=img_crop.copy()
                
                for cnt in contours:
                    cv2.drawContours(cropcopy, contours, -1, (0,0,255),5)
                sfunc.cView(cropcopy)
                
                return(len(contours))