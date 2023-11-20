import threading
import psutil
import matplotlib.pyplot as plt
import cv2
import time
import io
import numpy as np
timestamps = []
cpu_usage = []
frames = []

def plot_cpu_usage():
    global timestamps, cpu_usage, frames

    while True:
        timestamp = time.time()
        cpu_usage_percent = psutil.cpu_percent()

        timestamps.append(timestamp)
        cpu_usage.append(cpu_usage_percent)

        # Create a figure and plot the CPU usage data
        fig = plt.figure()
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.plot(timestamps, cpu_usage)
        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('CPU Usage (%)')
        ax1.set_title('CPU Usage in Real Time')
        ax1.set_xlim(min(timestamps), max(timestamps))
        ax1.set_ylim(0, 100)

        # Capture the plot as an image
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        frame = plt.imread(buf)

        # Add the plot image to the frames list
        frames.append(frame)

        # Clear the plot data and figure
        timestamps.clear()
        cpu_usage.clear()
        plt.close(fig)

        # Pause for a short interval
        time.sleep(0.1)

def capture_webcam_stream():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if ret:
            # Convert the frame to RGB format
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Add the webcam frame to the frames list
            frames.append(rgb_frame)

        # Limit the frame rate to reduce processing overhead
        time.sleep(1/30)  # 30 frames per second

def display_combined_stream():
    while True:
        if len(frames) > 1:
            # Combine the CPU usage plot image and the webcam frame into a single image
            combined_frame = np.concatenate([frames[0], frames[1]], axis=1)

            # Display the combined frame
            plt.imshow(combined_frame)
            plt.title('CPU Usage and Webcam Stream')

            # Update the plot and draw it
            plt.draw()

            # Remove the processed frames
            frames.pop(0)
            frames.pop(0)

            # Wait for a short interval to avoid overloading the GUI
            time.sleep(0.01)


# Create and start the threads for CPU usage plotting, webcam streaming, and combined stream display
cpu_usage_thread = threading.Thread(target=plot_cpu_usage)
webcam_stream_thread = threading.Thread(target=capture_webcam_stream)
combined_stream_thread = threading.Thread(target=display_combined_stream)

cpu_usage_thread.start()
webcam_stream_thread.start()
combined_stream_thread.start()

# Wait for the threads to finish
cpu_usage_thread.join()
webcam_stream_thread.join()
combined_stream_thread.join()

cv2.destroyAllWindows()
