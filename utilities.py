import cv2
import matplotlib.pyplot as plt
import numpy as np

def FaceDetection(img,screenWidth,screenHight):
    imgGrayScale=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    print('imagegrayscale')
    faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    print('objectCascadeClassifier done')

    DophinoTechfaces=faceCascade.detectMultiScale(imgGrayScale,1.1,4)
    print('objectCascadeClassifier done')

    centerOfFace=[]
    faceArea=[]
    for (x,y,w,h) in DophinoTechfaces:
        #it draw only horizental or vertcical rectangles
       # label = "Mohamed Amine SAADA"
        label = ("Mohamed Amine Saada")

        label_position = (x, y - 10)
        cv2.putText(img, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.line(img,(0,y+w//2),(x,y+w//2) , (0,0,255), 2)
        cv2.line(img, (x+w,y+w//2),(screenWidth,y+w//2), (0,0,255), 2)
        cv2.line(img, (x+w//2,0), (x+w//2,y), (0,0,255), 2)
        cv2.line(img,  (x+w//2,y+h), (x+w//2,screenHight), (255,0,255), 2)




        centerx=x+(w//2)
        centery=y+h//2
        area=w*h
        centerOfFace.append([centerx,centery])
        faceArea.append(area)

    if len(faceArea)!=0:
        #index of the face that have the maximal area
        i=faceArea.index(max(faceArea))
        return img,[faceArea[i],centerOfFace[i]]
    else:

        return img,[0,[0,0]]


def faceTracking(infos,PID, w, h, errorPidPrecedent):


    theTarget = w // 2
    # calculating the error of The PID controller
    errorPid = infos[1][0] - theTarget
    P = PID[0] * errorPid
    # we don't require a Integrater in our case
    I = 0
    D = PID[2] * (errorPid - errorPidPrecedent)
    speed = P + I + D
    # clip in numpy make the speed don't go out the interval -100 *** 100 if speed>100 the speed go above 100 it will be fixed as 100 and same
    speed = np.clip(int(speed), -100, 100)
    print(f"The speed from the PID controller{infos}")


    errorPidPrecedent = errorPid
    if infos==[0,[0,0]]:
        speed=0

    return errorPidPrecedent,speed