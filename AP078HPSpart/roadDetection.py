import cv2
import numpy as np
import imutils
import os,sys

def medianBlur(img):
	img = cv2.medianBlur(img,5)
	return img

def gaussianBlur(img):
	img = cv2.GaussianBlur(img, (7,7), 200)
	return img
	
def cannyImg(img):
	img = cv2.Canny(img,200,300)
	return img
	
def sobelImg(img):
	img = cv2.Sobel(src=img, ddepth=cv2.CV_64F, dx=2, dy=2, ksize=9) 
	return img

def displayhoughLines(image, lines):
	lines_image = np.zeros_like(image)
	if lines is not None:
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
			cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 10)
	return image

def displayhoughLinesP(image,lines):
	if lines is not None:
		for line in lines[0]:
			x1, y1, x2, y2 = line
			cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 10)
	return image


def houghLines(thresh):
	lines = cv2.HoughLines(thresh, 1, np.pi/180.0, 100)
	return lines

def houghLinesP(thresh):
	lines = cv2.HoughLinesP(thresh, 1, np.pi/180, 50)
	return lines


video = cv2.VideoCapture("videos/emptyRoad.mp4")

while video.isOpened():
	_, videoFrame = video.read()
	#videoFrame = cv2.imread('pngs/cementRoad.jpg')
	bgrFrame = cv2.cvtColor(videoFrame, cv2.COLOR_RGB2BGR)
	grayFrame = cv2.cvtColor(videoFrame, cv2.COLOR_RGB2GRAY)
	
	
	#denoise frames
	grayblurred = gaussianBlur(grayFrame)
	grayblurred = medianBlur(grayblurred)
	
	bgrblurred =  gaussianBlur(bgrFrame)
	bgrblurred = medianBlur(bgrblurred)
	
	#canny edges
	grayCanny = cannyImg(grayblurred)
	bgrCanny = cannyImg(bgrblurred)
	
	#sobel edges
	graySobel = sobelImg(grayblurred)
	bgrSobel = sobelImg(bgrblurred)
	
	
	#threshold IMG
	bgr2gray = cv2.cvtColor(videoFrame,cv2.COLOR_RGB2GRAY)
	threshBGRSobel = cv2.adaptiveThreshold(bgr2gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,31,60)
	
	bgblurred =  gaussianBlur(threshBGRSobel)
	bgblurred = medianBlur(bgblurred)
	bgrCanny = cannyImg(bgrblurred)
	
	lines = houghLinesP(bgrCanny)
	threshholdImg= displayhoughLinesP(bgrCanny,lines)
	#cv2.adaptiveThreshold(img_grey,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	
	
	grayCanny = imutils.resize(grayCanny, height = 300)
	bgrCanny = imutils.resize(bgrCanny, height = 300)
	bgrSobel = imutils.resize(bgrSobel, height = 300)
	graySobel = imutils.resize(graySobel, height = 300)
	threshBGRSobel = imutils.resize(threshholdImg, height = 300)
	
	
	cv2.imshow("bgrCanny", bgrCanny)
	cv2.imshow("grayCanny",grayCanny)
	cv2.imshow("bgrSobel", bgrSobel)
	cv2.imshow("graySobel",graySobel)
	cv2.imshow("threshBGRSobel",threshBGRSobel)
	
	if cv2.waitKey(1) == 27 or 0xff == ord('q'):
		break

video.release()
cv2.destroyAllWindows()


