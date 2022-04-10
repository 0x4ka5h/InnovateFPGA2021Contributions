import cv2
import numpy as np
import matplotlib.pyplot as plt
import colorhist
import plotAnglePoints
# load a video
#video = cv2.VideoCapture('videos/sideRoad.mp4')

# You can set custom kernel size if you want.
kernel = None

# Initialize the background object.
backgroundObject = cv2.createBackgroundSubtractorMOG2(20,detectShadows = True)

def detectObjectsMask(frame):

    y= frame.shape[0]
    x=frame.shape[1]

    
    leftShape = [(int(0), int(y)), (int(x*0.3), int(y)), (int(x*0.3),int(y*0.3)),(int(0),int(y*0.3))]
    leftCropped = colorhist.region_of_interest(frame,np.array([leftShape],np.int32),)
    
    #_ = frame[int(x*0.3):100, int(x*0.3):500]
    #cv2.imshow("ui",_)



    centerShape = [(int(x*0.3), int(y)),(int(x*0.7),int(y)), (int(x*0.7),int(y*0.3)),(int(x*0.3),int(y*0.3))]
    centerCropped = colorhist.region_of_interest(frame,np.array([centerShape],np.int32),)

    rightShape = [(int(x*0.7), int(y)),(int(x),int(y)), (int(x),int(y*0.3)),(int(x*0.7),int(y*0.3))]
    rightCropped = colorhist.region_of_interest(frame,np.array([rightShape],np.int32),)

    Lfgmask = backgroundObject.apply(leftCropped)
    Cfgmask = backgroundObject.apply(centerCropped)
    Rfgmask = backgroundObject.apply(rightCropped)
    #initialMask = fgmask.copy()
    _, Lfgmask = cv2.threshold(Lfgmask, 250, 255, cv2.THRESH_BINARY)
    _, Cfgmask = cv2.threshold(Cfgmask, 250, 255, cv2.THRESH_BINARY)
    _, Rfgmask = cv2.threshold(Rfgmask, 250, 255, cv2.THRESH_BINARY)
    #noisymask = fgmask.copy()
    
    Lfgmask = cv2.erode(Lfgmask, kernel, iterations = 1)
    Lfgmask = cv2.dilate(Lfgmask, kernel, iterations = 2)
    
    Cfgmask = cv2.erode(Cfgmask, kernel, iterations = 1)
    Cfgmask = cv2.dilate(Cfgmask, kernel, iterations = 2)
    
    Rfgmask = cv2.erode(Rfgmask, kernel, iterations = 1)
    Rfgmask = cv2.dilate(Rfgmask, kernel, iterations = 2)
    
    #for fgmask in [Lfgmask,Cfgmask,Rfgmask]:
    contours, _ = cv2.findContours(Lfgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frameCopyL = leftCropped.copy()
    countL=0
    for cnt in contours:
        if cv2.contourArea(cnt) > 400:
            countL+=1
            x, y, width, height = cv2.boundingRect(cnt)
            cv2.rectangle(frameCopyL, (x , y), (x + width, y + height),(0, 0, 255), 2)
            cv2.putText(frameCopyL, 'objectDetected', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,0), 1, cv2.LINE_AA)
    cv2.putText(frameCopyL, str(countL), (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,0), 2, cv2.LINE_AA)
    frameCopyL = plotAnglePoints.processPoints(frameCopyL)
    print(countL)
    #foregroundPart = cv2.bitwise_and(frame, frame, mask=fgmask)
    
    
    contours, _ = cv2.findContours(Cfgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #print(_)
    frameCopyC = centerCropped.copy()
    countC = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > 400:
            countC+=1
            x, y, width, height = cv2.boundingRect(cnt)
            cv2.rectangle(frameCopyC, (x , y), (x + width, y + height),(0, 0, 255), 2)
            cv2.putText(frameCopyC, 'objectDetected', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,0), 1, cv2.LINE_AA)
    cv2.putText(frameCopyC, str(countC), (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,0), 2, cv2.LINE_AA)
    frameCopyC = plotAnglePoints.processPoints(frameCopyC)
    print(countC)
    #foregroundPart = cv2.bitwise_and(frame, frame, mask=fgmask)
    
    
    contours, _ = cv2.findContours(Rfgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frameCopyR = rightCropped.copy()
    countR = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            countR+=1
            x, y, width, height = cv2.boundingRect(cnt)
            cv2.rectangle(frameCopyR, (x , y), (x + width, y + height),(0, 0, 255), 2)
            cv2.putText(frameCopyR, 'objectDetected', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,0), 1, cv2.LINE_AA)
    cv2.putText(frameCopyR, str(countR), (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,0), 2, cv2.LINE_AA)
    frameCopyR = plotAnglePoints.processPoints(frameCopyR)
    #foregroundPart = cv2.bitwise_and(frame, frame, mask=fgmask)
    print(countR)
    #cv2.imshow("dsf",frameCopyL)
    
    
    stacked = np.hstack((frameCopyL, frameCopyC, frameCopyR))
    cv2.imshow('Original Frame, Extracted Foreground and Detected Cars', cv2.resize(stacked, None, fx=0.5, fy=0.5))
    #cv2.imshow('initial Mask', initialMask)
    #cv2.imshow('Noisy Mask', noisymask)
    #cv2.imshow('Clean Mask', fgmask)

    # Wait until a key is pressed.
    # Retreive the ASCII code of the key pressed
    cv2.waitKey(1)


def safePointEstimation(frame):
	
	
	
	return
