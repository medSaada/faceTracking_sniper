import cv2
import numpy as np
from djitellopy import Tello

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
def initializeTello():
    DophinoTechDrone=Tello()
    DophinoTechDrone.connect()
    DophinoTechDrone.for_back_velocity=0
    DophinoTechDrone.left_right_velocity=0
    DophinoTechDrone.up_down_velocity=0
    DophinoTechDrone.yaw_velocity=0
    DophinoTechDrone.speed=0
    # Security First kids haha
    print(DophinoTechDrone.get_battery())
    DophinoTechDrone.streamoff()
    DophinoTechDrone.streamon()
    return DophinoTechDrone

def get_the_stream(dophinoTech,w=340,h=240):
    stream=dophinoTech.get_frame_read().frame
    imgstream=cv2.resize(stream,(w,h))
    return imgstream




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
        cv2.line(img,  (x+w//2,y+h), (x+w//2,screenHight), (0,0,255), 2)




        centerx=x+(w//2)
        centery=y+h//2
        area=w*h
        centerOfFace.append([centerx,centery])
        faceArea.append(area)

    if len(faceArea)!=0:
        #index of the face that have the maximal area
        i=faceArea.index(max(faceArea))
        return img,[centerOfFace[i],faceArea[i]]
    else:

        return img,[[0,0],0]


def faceTracking(DophinoTechDrone,infos,PID, w,  errorPidPrecedent):


    theTarget = w // 2
    # calculating the error of The PID controller
    errorPid = infos[0][0] - theTarget
    P = PID[0] * errorPid
    # we don't require a Integrater in our case
    I = 0
    D = PID[2] * (errorPid - errorPidPrecedent)
    speed = P + I + D
    # clip in numpy make the speed don't go out the interval -100 *** 100 if speed>100 the speed go above 100 it will be fixed as 100 and same
    speed = np.clip(int(speed), -100, 100)
    speed = int(np.clip(speed, -100, 100))
    print(f"The speed from the PID controller{speed}")
    if infos[0][0]!=0:
        DophinoTechDrone.yaw_velocity =speed
    else:
        DophinoTechDrone.for_back_velocity  =0
        DophinoTechDrone.left_right_velocity  =0
        DophinoTechDrone.up_down_velocity =0
        DophinoTechDrone.yaw_velocity =0
        errorPid = 0
        speed=0



    if DophinoTechDrone.send_rc_control:
        DophinoTechDrone.send_rc_control(DophinoTechDrone.left_right_velocity, DophinoTechDrone.for_back_velocity,DophinoTechDrone.up_down_velocity, DophinoTechDrone.yaw_velocity)
        print(f"We send a yaw speed to our drone{speed}")





    return errorPid,speed
