import cv2
import pickle
import os
import keyboard

firstClick=True
x1,y1=0,0
image = "GOPR0024.JPG"
imageIndex = 0

try:
    with open('carParkPos','rb') as f:
        posList=pickle.load(f)
except:
    posList=[]

def resizeFrame(frame, width=720, height=480):
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

def mouseClick(events,x,y,flags,params):
    global firstClick,x1,y1,imageIndex
    if events==cv2.EVENT_LBUTTONDOWN:
        if firstClick:
            x1,y1= x,y
            firstClick=False
        else:
            posList.append([x1,y1, x,y, imageIndex])
            firstClick=True
            print("Rectangle added")
        print("pressed L")
    if events==cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1=pos[0],pos[1]
            x2,y2=pos[2],pos[3]
            if x>x1 and x<x2 and y>y1 and y<y2:
                posList.pop(i)
    with open('carParkPos','wb') as f:
        pickle.dump(posList,f)

def changeImage():
    global imageIndex, image
    file_names = [f for f in os.listdir('images') if os.path.isfile(os.path.join('images', f))]
    image = file_names[imageIndex]

while True:
    img=cv2.imread(f"images/{image}")
    img = resizeFrame(img)
    for pos in posList:
        if pos[4]==imageIndex:
            cv2.rectangle(img, (pos[0], pos[1]) , (pos[2], pos[3]) ,(0,0,255),2)
    cv2.imshow("Image",img)
    cv2.setMouseCallback("Image",mouseClick)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('n'):
        imageIndex+=1
        changeImage()

cv2.destroyAllWindows()