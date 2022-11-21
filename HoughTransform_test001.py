import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

def showImg(image):
    plt.axis("off")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()

org_image = mpimg.imread('test001.jpg')
image = org_image[48:170, 0:215]
gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)

kernel_size = 5
blur_gray = cv2.GaussianBlur(gray,(kernel_size,kernel_size),0)

low_threshold = 50
high_threshold = 150
masked_edges = cv2.Canny(blur_gray,low_threshold,high_threshold)

rho = 1
theta = np.pi/360
threshold = 55
min_line_length = 30
max_line_gap = 20

line_image = np.copy(image)*0 #creating a blank to draw lines on

# line = np.array([])
lines = cv2.HoughLinesP(masked_edges,rho,theta,threshold,np.array([]),min_line_length,max_line_gap)


for axis in lines:
    x1,y1,x2,y2 = axis[0]
    cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)

color_edges = np.dstack((masked_edges,masked_edges,masked_edges))

combo = cv2.addWeighted(color_edges, 0.8, line_image, 1, 0) 
#plt.imshow(combo)
showImg(combo)