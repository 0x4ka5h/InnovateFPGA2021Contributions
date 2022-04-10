import cv2
import numpy as np
from matplotlib import pyplot as plt
def make_coordinates(image,line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1,y1,x2,y2])
def average_slope_intercept(image,lines):
    left_fit = []
    rightfit = []
    for line in lines:
        x1,y1,x2,y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2),(y1, y2),1)#we can get slop m and y intercept
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope,intercept))#we can get left line slop m and y intercept
        else:
            rightfit.append((slope,intercept))#we can get right line slop m and y intercept
    left_fit_avg = np.average(left_fit,axis = 0)
    rightfit_avg = np.average(rightfit, axis = 0)
    left_line = make_coordinates(image,left_fit_avg)
    right_line = make_coordinates(image,rightfit_avg)
    return np.array([left_line, right_line])

def Canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    gradiant = cv2.Canny(blur, 50, 150)
    return gradiant
def display_lines(image,lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)#already a one directional array we can remove it
            cv2.line(line_image,(x1,y1),(x2,y2),(0,255,255),10)
    return line_image

def region_of_interest(image):
    height = image.shape[0]
    triangle = np.array([[(200,height),(1100,height),(550,250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, triangle, 255)
    masked_img = cv2.bitwise_and(image,mask)
    return masked_img
#image = cv2.imread("test_image.png")
cap = cv2.VideoCapture("videos/emptyRoad.mp4")
while cap.isOpened():
    _,image = cap.read()

    lane_image = np.copy(image)  # we dont what to assign a "image" variable to lane_image coz if update an array that will reflacts on image.so we always choose copy while we are dealing with an arrays
# 1 convertimage to grayscale
#cv2.imshow("gray",gray)
#cv2.imshow("blur",blur)
    cropped_img = region_of_interest(Canny(lane_image))
    lines = cv2.HoughLinesP(cropped_img,2,np.pi/180,100,np.array([]),minLineLength = 50,maxLineGap=5)
    average_lines = average_slope_intercept(lane_image,lines)
    line_image = display_lines(lane_image,average_lines)
    adding_images = cv2.addWeighted(lane_image,0.8,line_image,1,1)
    cv2.imshow("result",adding_images)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()
