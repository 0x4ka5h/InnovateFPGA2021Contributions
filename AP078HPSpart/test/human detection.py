import numpy as np
from PIL import Image, ImageCms
import cv2
#cap = cv2.VideoCapture('')
humanCascade = cv2.CascadeClassifier('cars.xml')
vehicleCascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
while(True):
    #ret, frame = cap.read()
    frame = cv2.imread("cars.webp")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    humans = humanCascade.detectMultiScale(gray)
    cars = vehicleCascade.detectMultiScale(gray)
    for (x,y,w,h) in humans:
         cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    for (x,y,w,h) in cars:
         cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1)==27 or 0xFF == ord('q'):
        break
#cap.release()
cv2.destroyAllWindows()
