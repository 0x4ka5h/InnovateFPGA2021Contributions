import cv2
import numpy as np
import imutils
import math

def medianBlur(img):
	img = cv2.medianBlur(img,5)
	return img

def gaussianBlur(img):
	img = cv2.GaussianBlur(img, (5,5), 200)
	return img

def cannyImg(img):
	img = cv2.Canny(img,100,200)
	return img

def sobelImg(img):
	img = cv2.Sobel(src=img, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=7) 
	return img

def houghLinesP(thresh):
	lines = cv2.HoughLinesP(thresh,2,np.pi/180,100,1,3)
	for i in range(0,lines.shape[0]):
		for x1,y1,x2,y2 in lines[i]:
			cv2.line(thresh,(x1,y1),(x2,y2),(0,255,0),2)
	return thresh
    
def region(image):
	height, width = image.shape
	triangle = np.array([[(0, height), (int(width*1/2), int(height*1/4)), (width, height)]])
	mask = np.zeros_like(image)
	mask = cv2.fillPoly(mask, triangle, 255)
	mask = cv2.bitwise_and(image, mask)
	return mask


def houghLines(thresh):
	lines = cv2.HoughLines(thresh, 1, np.pi/180.0, 100, np.array([]), 0, 0)

	for line in lines:
		rho, theta = line[0]
		a = np.cos(theta)
		b = np.sin(theta)
		x0 = a*rho
		y0 = b*rho
		x1 = int(x0 + 1000*(-b))
		y1 = int(y0 + 1000*(a))
		x2 = int(x0 - 1000*(-b))
		y2 = int(y0 - 1000*(a))

		cv2.line(thresh,(x1,y1),(x2,y2),(0,0,255),2)
	return thresh



cap = cv2.VideoCapture("videos/emptyRoad.mp4")

while cap.isOpened():
	_,img = cap.read()
	img_grey = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

	thresh = cv2.adaptiveThreshold(img_grey,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,29,20)
	thresh = cv2.adaptiveThreshold(thresh,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,69,58)
	canny = cannyImg(thresh)
	#thresh = houghLines(canny)
	img = imutils.resize(thresh, height = 200)
	canny = imutils.resize(canny, height = 200)


	cv2.imshow('original', img)
	cv2.imshow('canny', canny)

	if cv2.waitKey(1) == 27 or 0xff == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()
