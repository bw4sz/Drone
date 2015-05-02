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
img_contours=img.copy()
for cnt in contours:
    area.append(cv2.contourArea(cnt))
    #get the max contour bounding box
    x,y,w,h=cv2.boundingRect(cnt)
    img_contours = cv2.rectangle(img_contours,(x,y),(x+w,y+h),(0,255,0),2)
    
#view contour
sfunc.cView(img_contours)

#find largest contour
themax=area.index(max(area))

#make a mask out of that area
mask = np.zeros(image.shape[:2], np.uint8)
mask=cv2.drawContours(mask, contours[themax], -1, 255, -1)

# Perform morphology
se = np.ones((200,200), dtype='uint8')
image_close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, se)
sfunc.cView(image_close)

##refind contours
#make a mask out of that area
image, contours, hierarchy = cv2.findContours(image_close,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
mask2 = np.zeros(image.shape[:2], np.uint8)

#fails to draw here.
mask2 = cv2.drawContours(mask2, contours, -1, (0,255,0), 3)

#find area
area = []
for cnt in contours:
    cv2.drawContours(mask2, cnt,0, (0,255,0), 2)
#view
sfunc.cView(mask2)

themax=area.index(max(area))
mask=cv2.drawContours(mask, contours[themax], -1, 255, -1)
sfunc.cView(mask)

#mask frame
img_crop=cv2.bitwise_and(img,img,mask=mask)
cv2.namedWindow("image cropped",cv2.WINDOW_NORMAL)
cv2.imshow("image cropped",img_crop)
cv2.waitKey(0)
cv2.destroyAllWindows()

##Cluster images

###get histogram of hsv 

#Turn to HSV color space
imgc_hsv=cv2.cvtColor(img_crop,cv2.COLOR_BGR2HSV)
cv2.namedWindow("hsv",cv2.WINDOW_NORMAL)
cv2.imshow("hsv",imgc_hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()

#calculate histogram
sfunc.drawHist(imgc_hsv)

#threshold colors

##what is a flag color? Its somewhere between white and red
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