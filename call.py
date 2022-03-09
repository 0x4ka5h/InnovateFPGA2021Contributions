import cv2
import requests
import base64

cap = cv2.VideoCapture('http://192.168.42.129:4747/video')
while cap.isOpened():
        p,f=cap.read()
        f=cv2.rotate(f, cv2.ROTATE_90_CLOCKWISE)
        #cv2.imshow('frame',f)
        #key=cv2.waitKey(1)
        #if key==27:
        #       break
        _,encoded = cv2.imencode('.png',f)
        en = base64.b64encode(encoded)
	en = en.decode('ascii')
        r= requests.post('http://10.4.32.38:5000/api/stream/send/',json={'imageData':en})
        print(r.content)

