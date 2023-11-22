import cv2
import time
import matplotlib.pyplot as plt
from utilities import *
import numpy as np
from djitellopy import Tello



#pid
PID=[0.5,0,0.5]
errorPidPrecedent=0
########################

#PLOTTING
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel('Time (seconds)', fontsize=14)
ax.set_ylabel('Speed', fontsize=14)
ax.set_title('The OUTPUT OF THE PID CONTOLLER ', fontsize=14)
ax.set_facecolor('black')
ax.grid(True, color='gray', linestyle='--', linewidth=0.5)

ax.set_ylim(-80, 80)
#fig.show()

i = 0
x, y = [], []
######################



#stream
#cap = cv2.VideoCapture(0)
################

#TELLO DRONE
DophinoTechDrone = initializeTello()

startCounter =0#  0 FOR FIGHT 1 FOR TESTING
##############


def getImg(display= False,size=[480,240]):
    _, img = cap.read()
    img = cv2.resize(img,(size[0],size[1]))
    if display:
        cv2.imshow('IMG',img)
    return img
###############################

#SAVE THE DATA

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('theResult.mp4', fourcc, 20.0, (640, 480))

####################



while True:
    i += 1
    if startCounter==0:
        DophinoTechDrone.takeoff()
        DophinoTechDrone.move_up(55)
        startCounter=1

    img = get_the_stream(DophinoTechDrone)
    #webCam tesing
    #img = getImg(True)
    frame, infos = FaceDetection(img, 480, 270)
    errorPidPrecedent, speed = faceTracking(DophinoTechDrone,infos, PID,420, errorPidPrecedent)


    #PLOTFig
    x.append(i)
    y.append(speed)

    ax.plot(x, y, color='b')
    #drow a  line
    ax.axhline(y=0, color='red', linestyle='-', linewidth=1.5)
    fig.canvas.draw()

    ax.set_xlim(left=max(0, i - 50), right=i + 50)
    fig.savefig('plot.png')
    img2 = cv2.imread('plot.png')
    img2 = np.uint8(img2)



    # Convert the NumPy array to uint8 format
    imgStacked = stackImages(0.7, [[img, img2]])
    # saving
    out.write(imgStacked)
    cv2.imshow('IMG', imgStacked)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

plt.close()

#cap.release()
cv2.destroyAllWindows()
# After we release our webcam, we also release the output
out.release()
