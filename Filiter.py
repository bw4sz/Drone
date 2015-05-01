#Ben Weinstein

#read in image, process for fisheye, run contour analysis

import cv2
import os
import numpy as np

#Read in file
file="C:/Users/Ben/Desktop/DJI01343.tif"
img=cv2.imread(file)

#view 
cv2.namedWindow("original",cv2.WINDOW_NORMAL)
cv2.imshow("original",img)
cv2.waitKey(0)

#Detect red flagging

#Turn to HSV color space
img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
cv2.namedWindow("hsv",cv2.WINDOW_NORMAL)
cv2.imshow("hsv",img_hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()

#threshold colors

#what is a flag color? Its somewhere between white and red
# i googled these colors
RED_MIN = np.array([0, 0, 20],np.uint8)
RED_MAX = np.array([10, 50, 50],np.uint8)

frame_threshed = cv2.inRange(src=img_hsv, lowerb=RED_MIN, upperb=RED_MAX)
cv2.namedWindow("threshold",cv2.WINDOW_NORMAL)
cv2.imshow("threshold",frame_threshed)
cv2.waitKey(0)
cv2.destroyAllWindows()
