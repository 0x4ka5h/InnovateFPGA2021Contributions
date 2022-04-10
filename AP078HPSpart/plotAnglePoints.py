import cv2
import numpy as np

def processPoints(image):
    #print(image.shape)
    h = image.shape[0]
    w = image.shape[1]
    p1=(0,int(0.3*h))
    p2=(int(0.5*w),int(0.3*h))
    p3=(w,int(0.3*h))
    p4=(int(0.3*w),int(0.44*h))
    p5=(int(0.7*w),int(0.44*h))
    p6=(0,int(0.72*h))
    p7=(int(0.3*w),int(0.72*h))
    p8=(int(0.5*w),int(0.58*h))
    p9=(int(0.7*w),int(0.72*h))
    p10=(w,int(0.72*h))
    cv2.circle(image,p1,1,(255,255,255),2)
    cv2.circle(image,p2,1,(255,255,255),2)
    cv2.circle(image,p3,1,(255,255,255),2)
    cv2.circle(image,p4,1,(255,255,255),2)
    cv2.circle(image,p5,1,(255,255,255),2)
    cv2.circle(image,p6,1,(255,255,255),2)
    cv2.circle(image,p7,1,(255,255,255),2)
    cv2.circle(image,p8,1,(255,255,255),2)
    cv2.circle(image,p9,1,(255,255,255),2)
    cv2.circle(image,p10,1,(255,255,255),2)
    return image

  
def drawWayPaths():
	return
