# # Import the recording process
# from camera_record import record_video
# # set recording duration
# record_time = 60
# # To run this as part of a bigger program, use mutltiprocessing to create a seperate process
# # for video recording using the following lines.
# from multiprocessing import Process
# # The line above can go to the top of your file and the following lines should be placed
# # where ever you need to record a video
# # Create the process thread object
# cam_record = Process(target=record_video, args=(record_time, ))
# cam_record.start()
# # The following statement waits till the process is completed before going to the next line of code
# cam_record.join()
# cam_record.close()
# # If recording a video is not part of a bigger program then you don't need to use multiprocesing
# # and can comment out the last 4 lines and uncomment the next line
# #record_time(record_time)

# ctrl / to comment out all lines highlighted

import queue
import threading
#import serial
import time
import PIL
from PIL import Image, ImageTk
import cv2
import subprocess
import datetime

# TODO - Save to a backup folder every 15min - if no errors occur these can be deleted at the end
#   otherwise we ave a backup

def StartCamera(duration=3600):
    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)

    # Set the video inpout
    cap.set(3, 1280)
    cap.set(4, 720)
    cap.set(cv2.CAP_PROP_FPS, 15)  # set FPS

    # Get the frames per second (fps) and the frame size
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    duration = duration * fps
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    date_time = datetime.datetime.now()
    date_time = date_time.strftime("%Y-%m-%d_%H-%M-%S")
    print(date_time)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('C:/Users/hsojh/PycharmProjects/Yolov7_StrongSORT_OSNet_MAIN/Output_{}.mp4'.format(date_time), fourcc, fps,
                          (frame_width, frame_height))
    print('C:/Users/hsojh/PycharmProjects/Yolov7_StrongSORT_OSNet_MAIN/Output_{}.mp4'.format(date_time))
    # Queue to store the frames
    frame_queue = queue.Queue()

    # Flag to indicate if the writing thread should stop
    stop_flag = False

    # Function to write the frames to the video file
    def write_frames():
        while not stop_flag:
            if not frame_queue.empty():
                # print(frame_queue.qsize())
                frame = frame_queue.get()
                out.write(frame)

    # Start the writing thread
    writing_thread = threading.Thread(target=write_frames)
    writing_thread.start()

    # Loop over the frames of the video
    frame_num = 0
    while frame_num < duration:
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame_num += 1

        # If the frame was properly read, add it to the queue
        if ret:
            frame_queue.put(frame)

        # Display the frame
        if frame_num == 0 or frame_num % 5 == 0:
            #pass
            new_frame = cv2.resize(frame, (640, 480))
            cv2.imshow('frame', new_frame)

        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Set the stop flag to True to indicate that the writing thread should stop
    stop_flag = True

    # Wait for the writing thread to finish
    writing_thread.join()

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()

    # Close all windows
    cv2.destroyAllWindows()


if __name__ == '__main__':
    record_duration=360
    StartCamera(record_duration)
    # ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    # ser.reset_input_buffer()
    # end_time = 0
    #
    # while True:
    #     line = ser.readline().decode('utf-8').rstrip()
    #     print(line)
    #
    #     if line[:4] == 'Start':
    #         duration = int(line[4:]) + 600  # give an extra 10min for start up and save time
    #         record_duration = duration - 600
    #         p = subprocess.run(StartCamera(record_duration), timeout=duration)
    #     if line[:8] == 'Btn_Click':
    #         subprocess.run('vcgencmd display_power 1', shell=True)  # Turn on the display
    #         # start timer - sleep after 15 min
    #         start_time = time.time()
    #         end_time = start_time + 15 * 60
    #     if (time.time() > end_time) and (end_time != 0):
    #         subprocess.run('vcgencmd display_power 0', shell=True)  # Turn off the display
    #         end_time = 0
    #
    #     time.sleep(1)


