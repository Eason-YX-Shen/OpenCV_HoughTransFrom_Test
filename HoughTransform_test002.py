import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

def showImg(image):
    plt.axis("off")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()

org_image = mpimg.imread('test003.jpg',-1)
image = org_image[48:170, 0:215]
gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
kernel_size = 5
blur_gray = cv2.GaussianBlur(gray,(kernel_size,kernel_size),0)

#ret,th = cv2.threshold(blur_gray,120,255,cv2.THRESH_BINARY)
ret,th = cv2.threshold(blur_gray,120,255,cv2.THRESH_TOZERO)

low_threshold = 50
high_threshold = 120
masked_edges = cv2.Canny(th,low_threshold,high_threshold)

rho = 1
theta = np.pi/3600
threshold = 50
min_line_length = 30
max_line_gap = 2

line_image = np.copy(image)*0 #creating a blank to draw lines on

# line = np.array([])
lines = cv2.HoughLinesP(masked_edges,rho,theta,threshold,np.array([]),min_line_length,max_line_gap)

#lines[陣列編號][固定為0][陣列中的值，0=x1, 1=y1, 2=x2, 3=y2]

col1 = 0
while col1 <= (len(lines) - 1):
    j = 0
    while j <= len(lines):
        if ((lines[col1][0][0] - lines[j][0][0])**2 + (lines[col1][0][1] - lines[j][0][1])**2)**0.5 < 50 and ((lines[col1][0][2] - lines[j][0][2])**2 + (lines[col1][0][3] - lines[j][0][3])**2)**0.5 < 50:
            lines = np.delete(lines, j, axis = 0);
        j += 1;
        if j >= len(lines):
            break;
    col1 += 1;
    if col1 >= len(lines) - 1:
        break;


if len(lines) == 2:
    cv2.line(line_image,(lines[0][0][0],lines[0][0][1]),(lines[0][0][2],lines[0][0][3]),(255,0,0),5)
    cv2.line(line_image,(lines[1][0][0],lines[1][0][1]),(lines[1][0][2],lines[1][0][3]),(255,0,0),5)
    for i in range(len(lines)):
        box1 = 0
        box2 = 0
        if lines[i][0][1] > lines[i][0][3]:
            box1 = lines[i][0][1];
            lines[i][0][1] = lines[i][0][3];
            lines[i][0][3] = box1
            box2 = lines[i][0][0];
            lines[i][0][0] = lines[i][0][2];
            lines[i][0][2] = box2;
    cv2.line(line_image,(int((lines[0][0][0]+lines[1][0][0])/2), int((lines[0][0][1]+lines[1][0][1])/2)),(int((lines[0][0][2]+lines[1][0][2])/2), int((lines[0][0][3]+lines[1][0][3])/2)),(0,255,0),5)

# for axis in lines:
#     x1,y1,x2,y2 = axis[0]
#     cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)

color_edges = np.dstack((masked_edges,masked_edges,masked_edges))

combo = cv2.addWeighted(color_edges, 0.8, line_image, 1, 0) 
#plt.imshow(combo)

showImg(combo)