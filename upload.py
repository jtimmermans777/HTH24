import cv2
import numpy as np
import pickle
import os
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import random as rand

MONGOPassword = os.getenv('MONGO_PASSWORD')
uri = "mongodb+srv://nuhinsalamun7:K8uCMdc3yobUquQu@parkingspot.htqfr.mongodb.net/"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['carPark']
collection = db['carParkData']

image = "GOPR0024.JPG"
imageIndex = 0
freeSpots = 0
totalSpots = 0

with open('carParkPos','rb') as f:
    posList=pickle.load(f)

def resizeFrame(frame, width=720, height=480):
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)

def check(imgPro):
    global imageIndex, freeSpots, totalSpots
    freeSpots = 0
    totalSpots = 0
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
                freeSpots+=1
                color=(0,255,0)
                thick=5
            else:
                color=(0,0,255)
                thick=2
            cv2.rectangle(img,(pos[0], pos[1]) , (pos[2], pos[3]), color, thick)
            totalSpots+=1
    if totalSpots == 0:
        exit()

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
    data = {
        "_id": imageIndex,
        "freeSpots": freeSpots,
        "totalSpots": totalSpots,
        #randomly generate coordinates
        "longitude": 42.3370 + (0.01449 * rand.randint(-20, 20)),
        "latitude": 71.2092 + (0.01449 * rand.randint(-20, 20))
    }
    try:
        result = collection.insert_one(data)
    except Exception as e:
        result = collection.update_one({"_id": imageIndex}, {"$set": data})
    # print(f'Data inserted with record id {result}')
    imageIndex+=1
    changeImage()

cv2.destroyAllWindows()