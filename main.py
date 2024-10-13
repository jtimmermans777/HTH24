import cv2
import numpy as np
import pickle
import os

image = "GOPR0024.JPG"
imageIndex = 0

with open('carParkPos','rb') as f:
    posList=pickle.load(f)

def resizeFrame(frame, width=720, height=480):
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

def check(imgPro):
    global imageIndex
    totalCount=0
    spaceCount=0
    for pos in posList:
        if pos[4]==imageIndex:
            x1=pos[0]
            y1=pos[1]
            x2=pos[2]
            y2=pos[3]
            crop=imgPro[y1:y2,x1:x2]
            # cv2.imshow("crop",crop)
            # cv2.waitKey(0)
            count=cv2.countNonZero(crop)
            # total=cv2.countNonZero(imgPro)
            if count<300:
                spaceCount+=1
                color=(0,255,0)
                thick=5
            else:
                color=(0,0,255)
                thick=2
            cv2.rectangle(img,(pos[0], pos[1]) , (pos[2], pos[3]), color, thick)
            totalCount+=1
    cv2.rectangle(img,(45,30),(250,75),(180,0,180),-1)
    cv2.putText(img,f'Free: {spaceCount}/{totalCount}',(50,60),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2)

def changeImage():
    global imageIndex, image
    file_names = [f for f in os.listdir('images') if os.path.isfile(os.path.join('images', f))]
    image = file_names[imageIndex]

while True:
    img = cv2.imread('images/' + image)
    img = resizeFrame(img)
    canny = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.GaussianBlur(img, (3, 3), 1)
    canny = cv2.Canny(canny, 125, 175)
    canny = cv2.threshold(canny, 127, 255, cv2.THRESH_BINARY)[1]
    
    check(canny)
    cv2.imshow("Display",canny)
    cv2.imshow("Image",img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('n'):
        imageIndex+=1
        changeImage()

cv2.destroyAllWindows()