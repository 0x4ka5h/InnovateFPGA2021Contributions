'''import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
import imutils

def invert_img(img):
    img = (255-img)
    return img

def canny(imgray):
    imgray = cv2.GaussianBlur(imgray, (5,5), 200)
    canny_low = 100
    canny_high = 200

    thresh = cv2.Canny(imgray,canny_low,canny_high)
    return thresh

def sobel(imgray):
	imgray = cv2.GaussianBlur(imgray, (5,5), 200)
	sobelxy = cv2.Sobel(src=imgray, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection
	return sobelxy
def filtering(imgray):
    thresh = canny(imgray)
    #thresh = sobel(imgray)

    minLineLength = 1
    maxLineGap = 3


    lines = cv2.HoughLines(thresh,1,np.pi/180,0)
    #lines = cv2.HoughLinesP(thresh,2,np.pi/180,100,minLineLength,maxLineGap)
    print(lines.shape)

    # Code for HoughLinesP
    #
    #for i in range(0,lines.shape[0]):
    #    for x1,y1,x2,y2 in lines[i]:
    #        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    

    # Code for HoughLines
    
    for i in range(0,5):
        for rho,theta in lines[i]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))

            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
    

    return thresh
cap = cv2.VideoCapture("curvedRoad.mp4")
while cap.isOpened():
	#img = cv2.imread('road.jpeg')
	_,img = cap.read()
	try:
		imgray = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

		img = imutils.resize(img, height = 500)
		imgray = imutils.resize(imgray, height = 500)

		thresh = filtering(imgray)

		cv2.imshow('original', img)
		cv2.imshow('result', thresh)
	except:
		break
	if cv2.waitKey(1) == 27 or 0xff == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()'''




#ROAD LANE DETECTION

import cv2
import matplotlib.pyplot as plt
import numpy as np
import imutils

def grey(image):
  #convert to grayscale
    image = np.asarray(image)
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

  #Apply Gaussian Blur --> Reduce noise and smoothen image
def gauss(image):
    return cv2.GaussianBlur(image, (5, 5), 0)

  #outline the strongest gradients in the image --> this is where lines in the image are
def canny(image):
    edges = cv2.Canny(image,50,150)
    return edges

def region(image):
    height, width = image.shape
    #isolate the gradients that correspond to the lane lines
    triangle = np.array([
                       [(0, height), (0,int(height*3/4)),(int(width*1/4),int(height*1/4)),(int(width*3/4),int(height*1/4)),(width,int(height*3/4)), (width, height)]
                       ])
    #create a black image with the same dimensions as original image
    mask = np.zeros_like(image)
    #create a mask (triangle that isolates the region of interest in our image)
    mask = cv2.fillPoly(mask, triangle, 255)
    mask = cv2.bitwise_and(image, mask)
    return mask

def display_lines(image, lines):
    lines_image = np.zeros_like(image)
    #make sure array isn't empty
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line
            #draw lines on a black image
            cv2.line(lines_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return lines_image

def average(image, lines):
    left = []
    right = []

    if lines is not None:
      for line in lines:
        print(line)
        x1, y1, x2, y2 = line.reshape(4)
        #fit line to points, return slope and y-int
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        print(parameters)
        slope = parameters[0]
        y_int = parameters[1]
        #lines on the right have positive slope, and lines on the left have neg slope
        if slope < 0:
            left.append((slope, y_int))
        else:
            right.append((slope, y_int))
            
    #takes average among all the columns (column0: slope, column1: y_int)
    right_avg = np.average(right, axis=0)
    left_avg = np.average(left, axis=0)
    #create lines based on averages calculates
    left_line = make_points(image, left_avg)
    right_line = make_points(image, right_avg)
    return np.array([left_line, right_line])

def make_points(image, average):
    print(average)
    slope, y_int = average
    y1 = image.shape[0]
    #how long we want our lines to be --> 3/5 the size of the image
    y2 = int(y1 * (3/5))
    #determine algebraically
    x1 = int((y1 - y_int) // slope)
    x2 = int((y2 - y_int) // slope)
    return np.array([x1, y1, x2, y2])

#from google.colab.patches import cv2_imshow
cap = cv2.VideoCapture("snowRoad.mp4")
while cap.isOpened():
	_,image1 = cap.read()
	plt.imshow(image1)


	copy = np.copy(image1)
	edges = cv2.Canny(copy,50,150)
	isolated = region(edges)
	edges = imutils.resize(edges, height = 200)
	isolated = imutils.resize(isolated, height = 200)
	cv2.imshow("edges",edges)
	cv2.imshow("isolated",isolated)

	#DRAWING LINES: (order of params) --> region of interest, bin size (P, theta), min intersections needed, placeholder array, 
	lines = cv2.HoughLinesP(isolated, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
	averaged_lines = average(copy, lines)
	black_lines = display_lines(copy, averaged_lines)
	#taking wighted sum of original image and lane lines image
	lanes = cv2.addWeighted(copy, 0.8, black_lines, 1, 1)
	lanes = imutils.resize(lanes, height = 200)
	cv2.imshow("lanes",lanes)
	if cv2.waitKey(1)==27 or 0xff==ord('q'):
		break
cap.release()
cv2.destroyAllWindows()
