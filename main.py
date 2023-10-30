import cv2
from utilities import *
import matplotlib.pyplot as plt
from collections import deque



w=340
h=240
#PID CONCTANTS VALUES
PID=[0.5,0,0.5]
speed_values = deque(maxlen=100)  # Adjust the maximum number of values to display on the plot
# plt.figure(figsize=(8, 6))
# plt.title('Speed Output Variation')
# plt.xlabel('Time')
# plt.ylabel('Speed')
# plt.ylim(-100, 100)  # Set y-axis limit to display speed range (-100 to 100)
# plt.grid()
plt.style.use('dark_background')

errorPidPrecedent=0
cap = cv2.VideoCapture(0)
fig, (ax1, ax2) = plt.subplots(2, 1)

if not cap.isOpened():
    print("Error: Could not access the webcam")
else:
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (w, h))
        frame,infos=FaceDetection(frame)
        errorPidPrecedent,speed = faceTracking(infos, PID, w, h, errorPidPrecedent)
        speed_values.append(speed)

        # Clear the plot and plot the updated speed values
        ax2.clear()
        ax2.plot(speed_values, color='red', linestyle='-', linewidth=1.5)  # Red curve
        ax2.set_title('Speed Output Variation', color='white', fontsize=14,fontweight='bold', y=2.2)  # Title with larger font and bold
        ax2.set_xlabel('Time', color='white', fontsize=10)  # X-axis label with larger font
        ax2.set_ylabel('Speed', color='white', fontsize=10)  # Y-axis label with larger font
        ax2.set_ylim(-100, 100)
        ax2.grid(True, color='gray')

        # Display the plot
        ax1.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        #plt.pause(0.01)
        #cv2.imshow('Tracker', frame)
        plt.pause(0.01)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
