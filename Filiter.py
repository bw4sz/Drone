#Ben Weinstein - Stony Brook University

#read in image, run contour analysis, count flowers

import cv2
import os
import numpy as np

#local source files
import sfunc

#Read in file
file="C:/Users/Ben/Desktop/DJI01343.tif"
img=cv2.imread(file)

#view 
sfunc.cView(img)

#Detect red flagging

#Turn to HSV color space
img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
sfunc.cView(img_hsv)

#threshold colors

#what is a flag color? Its somewhere between white and red
# i googled these colors
RED_MIN = np.array([160, 120, 120],np.uint8)
RED_MAX = np.array([180, 255, 255],np.uint8)

frame_threshed = cv2.inRange(src=img_hsv, lowerb=RED_MIN, upperb=RED_MAX)
sfunc.cView(frame_threshed)

#inflate sections to remove any small blips
kernel = np.ones((40,40),np.uint8)
closing = cv2.dilate(frame_threshed, kernel,3)
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
img_crop=cv2.bitwise_and(img,img,mask=mask2)
sfunc.cView(img_crop)

###Cluster images

###get histogram of hsv 

#Turn to HSV color space
imgc_hsv=cv2.cvtColor(img_crop,cv2.COLOR_BGR2HSV)
sfunc.cView(imgc_hsv)

#threshold colors

##what is a flower color? Its somewhere between white and red
## i googled these colors
WHITE_MIN = np.array([0, 0, 220],np.uint8)
WHITE_MAX = np.array([180, 50, 255],np.uint8)

frame_threshed = cv2.inRange(src=imgc_hsv, lowerb=WHITE_MIN, upperb=WHITE_MAX)
cv2.namedWindow("threshold",cv2.WINDOW_NORMAL)
cv2.imshow("threshold",frame_threshed)
cv2.waitKey(0)
cv2.destroyAllWindows()

#view segmented imaged
cropthresh=cv2.bitwise_and(img_crop,img_crop,mask=frame_threshed)
cv2.namedWindow("threshold",cv2.WINDOW_NORMAL)
cv2.imshow("threshold",cropthresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

##inflate sections to remove any small blips
#kernel = np.ones((40,40),np.uint8)
#closing = cv2.dilate(frame_threshed, kernel,3)
#cv2.namedWindow("threshold",cv2.WINDOW_NORMAL)
#cv2.imshow("threshold",closing)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

##draw contours 
#image, contours, hierarchy = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)