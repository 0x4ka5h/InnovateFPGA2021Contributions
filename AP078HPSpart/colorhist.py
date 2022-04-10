import cv2
import numpy as np
import subprocess
import detect2

def find_points(image):
	x=image.shape[1]
	y=image.shape[0]
	print(image.shape)
	pixel=255
	yl=0
	yr=0
	for i in range(y-1,-1,-1):
	    	if image[i,10]==pixel:
	    		yl=i;break
	for j in range(y-1,-1,-1):
	    	if image[j,x-10]==pixel:
	    		yr=j;break
	return yl,yr
		            	
def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image
    
def processor(img,l):

	img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#cv2.imshow('gray',img)
	gas=cv2.GaussianBlur(img,(11,11),3)
	
	y = gas.shape[0]
	x = gas.shape[1]
	
	
	l = [(int(0), int(y)), (int(x), int(y)), (int(x),int(y*0.3)),(int(0),int(y*0.3))]
	#gas = gas[int(y*0.35):,:]
	#cv2.imshow("dsf",gas)
	
	cany=cv2.Canny(gas,100,170)
	y= img.shape[0]
	x=img.shape[1]
	shape = [(int(0), int(y*0.6)), (int(x), int(y*0.6)), (int(x),int(y*0.4)),(int(0),int(y*0.4))]
	cropped_image = region_of_interest(cany,np.array([shape],np.int32),)    
	
	mask2=cv2.adaptiveThreshold(cropped_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,15,3)
	kernel=np.ones((5,5),np.uint8)
	#cv2.imshow("threshold",cany)
	dilation=cv2.dilate(cany,kernel,iterations=2)
	#list1=[i for i in dilation[0:dilation.shape[1]] ]
	ld,rd=find_points(dilation)
	p=ld-rd
	#print("Difference",p)
	#print("Ld =>",ld, "rd =>", rd)
	l.append(p)
	#print("dilation print=> ",p)
	if (p<-50):
	# 	subprocess.Popen(['sh','left.sh'])
		print("Decision: Steer Left")
		#subprocess.Popen(['sh','left.sh'])
		#subprocess.Popen(['sh','noright.sh'])
	# 	subprocess.Popen(['sh','noright.sh'])
	elif(p>50):
		print("Decision: Steer Right")
		#subprocess.Popen(['sh','right.sh'])
		#subprocess.Popen(['sh','noleft.sh'])
	else:
		print("Decision: Steer Forward")
		#subprocess.Popen(['sh','noright.sh'])
		#subprocess.Popen(['sh','noleft.sh'])
	#cv2.imshow("dialtion",dilation)
	return dilation,l
def draw_lines(img, lines, color=[0,0,255], thickness=3):
    line_img = np.zeros(
        (
            img.shape[0],
            img.shape[1],
            3
        ),
        dtype=np.uint8,
    )    # Loop over all lines and draw them on the blank image.
    try:
        for line in lines:
            print(line)
            for x1, y1, x2, y2 in line:
                cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
                                                        # Merge the image with the lines onto the original.
        img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)    # Return the modified image.
        return img
    except:
        pass
l=[]
#cap=cv2.VideoCapture("videos/sideRoad.mp4")
#while True:
#	#img = cv2.imread('pngs/cementRoad.jpg')
#	_,img=cap.read()
#	cv2.imshow('frame',img)
def run(img):
	global l
	dilated,list1=processor(img,l)
	#try:
	lines = cv2.HoughLinesP(
		dilated,
		rho=6,
		theta=np.pi / 60,
		threshold=600,
		lines=np.array([]),
		minLineLength=100,
		maxLineGap=15
		)
	final_image = draw_lines(img, lines)

#		cv2.imshow("Final Image",final_image)
#		cv2.waitKey(1)
	return final_image
#	except:
#		print("Move Forward for exception")
#		subprocess.Popen(['sh','right.sh'])
#		subprocess.Popen(['sh','left.sh'])
#		return

'''
while True:
	#img = cv2.imread('pngs/cementRoad.jpg')
	_,img=cap.read()
	#cv2.imshow('frame',img)
	img_ = run(img)
	print(img_)
	try:
		cv2.imshow("f",img_)
		print(2)
	except:
		#cv2.imshow("f",img)
		pass
	if cv2.waitKey(1)==27:
		break
'''

cv2.destroyAllWindows()
