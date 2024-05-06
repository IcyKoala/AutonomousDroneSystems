import cv2 
import numpy as np 
import math
from matplotlib import pyplot as plt 
  
# reading image 
img = cv2.imread('image1.png')


  
# converting image into grayscale image 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
  
# setting threshold of gray image 
_, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY) 
  
# using a findContours() function 
contours, _ = cv2.findContours( 
    threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
  
i = 0
  
# list for storing names of shapes 
for contour in contours: 
    
  
    # here we are ignoring first counter because  
    # findcontour function detects whole image as shape 
    if i == 0: 
        i = 1
        continue
  
    # cv2.approxPloyDP() function to approximate the shape 
    approx = cv2.approxPolyDP( 
        contour, 0.01 * cv2.arcLength(contour, True), True) 
    
    # using drawContours() function 
    cv2.drawContours(img, [contour], 0, (0, 0, 255), 5) 
  
    maxIndex = 0
    max = 0
    print(approx)
    for index in range(len(approx)):
        line1 = math.hypot(approx[index][0][0] - approx[index-1][0][0], approx[index][0][1] - approx[index-1][0][1])
        line2 = math.hypot(approx[index][0][0] - approx[index-2][0][0], approx[index][0][1] - approx[index-2][0][1])
        if line1 + line2 > max:
            max = line1 + line2
            maxIndex = index
    print(approx[maxIndex])
    # finding center point of shape 
    M = cv2.moments(contour) 
    if M['m00'] != 0.0: 
        x = int(M['m10']/M['m00']) 
        y = int(M['m01']/M['m00'])
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
# displaying the image after drawing contours 
cv2.imshow('shapes', img) 
  
cv2.waitKey(0) 
cv2.destroyAllWindows() 