from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import serial
import time
import statsmodels.api as sm

arduino = serial.Serial('COM4',9600)
time.sleep(2)

def nothing(x):
    pass

cv2.namedWindow("Tracking")
cv2.createTrackbar("LH", "Tracking", 17, 255, nothing)
cv2.createTrackbar("LS", "Tracking", 119, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 119, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 32, 255, nothing)
cv2.createTrackbar("US", "Tracking", 163, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 251, 255, nothing)


# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-v", "--video", help="path to the (optional) video file")
#ap.add_argument("-b", "--buffer", type=int, default=30, help="max buffer size")
#args = vars(ap.parse_args())

pts = deque(maxlen=30)
slope_average = deque(maxlen=30)
counter = 0
(dx, dy) = (0, 0)
threshold = 100
top_gutter = 50
bottom_gutter = 400
target_zone = 500
current_position_pixels = 0
number_of_steps = 0
rest_position = 200
response = ''
radius = 0




# list of tracked points

#pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam

vs = VideoStream(src=0).start()

#cap = cv2.VideoCapture(0)


# allow the camera or video file to warm up

# keep looping
while True:
    # grab the current frame



    frame = vs.read()
    #ret, frame = cap.read()

    frame = cv2.flip(frame,1)
    frame = cv2.line(frame,(threshold,0),(threshold,600),(255,255,0),2,8,0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    frame = cv2.line(frame,(0,bottom_gutter),(600,bottom_gutter),(0,255,0),2,8,0)
    frame = cv2.putText(frame,"bottom_gutter",(200,bottom_gutter-10), font, .5, (0,255,255), 1, cv2.LINE_AA)
    frame = cv2.line(frame, (0, top_gutter), (600, top_gutter), (0, 255, 0), 2, 8, 0)
    frame = cv2.putText(frame, "top_gutter", (200, top_gutter - 10), font, .5, (0, 255, 255), 1, cv2.LINE_AA)
    frame = cv2.line(frame, (target_zone, top_gutter), (target_zone, bottom_gutter), (0,0,255), 2, 8, 0)


    # handle the frame from VideoCapture or VideoStream
    #frame = frame[1] if args.get("video", False) else frame

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break


    blurred = cv2.GaussianBlur(frame, (41, 41), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")
    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")



    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])


    mask = cv2.inRange(hsv, l_b, u_b)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cv2.imshow("Tracking",mask)






    # find contours in the mask and initialize the current

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    else:

            cv2.circle(frame, (target_zone, rest_position), 5, (255, 0, 255), -1)
            #arduino.write((str(rest_position) + '\n').encode())
            current_position_pixels = rest_position










        # only proceed if the radius meets a minimum size
    if radius > 10:
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
        cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 0) , 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        # update the points queue
    pts.appendleft(center)




    # loop over the set of tracked points
    for i in np.arange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # check to see if enough points have been accumulated in
        # the buffer
        if counter >= 20 and i == 1 and pts[-10] is not None:

            dx = pts[-10][0] - pts[i][0]
            dy = pts[-10][1] - pts[i][1]
            pts1 = np.transpose(pts)
            x1 = pts1[0]
            y1 = pts1[1]
            X = sm.add_constant(x1)
            model = sm.OLS(y1,X)
            results = model.fit()


            if dx == 0 or dx > 0 or center[0] < threshold or center[1] > bottom_gutter or center[1] < top_gutter or center[0] > target_zone:
                continue
            else:
                #slope = dy / dx
                slope = results.params[1]

                #This should help remove some of the outlier values by using the average of the last 30 measurements

                slope_average.appendleft(slope)
                smoothed_slope = np.mean(slope_average)
                projected_target = int(smoothed_slope * (target_zone - center[0]) + center[1])

                #projected_target = int(slope * (target_zone - center[0]) + center[1])

                if projected_target < top_gutter or projected_target > bottom_gutter:
                    continue

                else:
                    frame = cv2.line(frame,center,(target_zone,projected_target),(0,0,255),3,8,0)
                    number_of_steps = projected_target - current_position_pixels
                    cv2.circle(frame, (target_zone, projected_target), 5, (255, 0, 255), -1)
                    current_position_pixels = projected_target
                    print("projected_target {}".format(projected_target))
                    arduino.write((str(projected_target) + '\n').encode())
                    #data = arduino.readline()
                    #if (data !=""):
                      #  print(data)









    # show the frame to our screen

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    counter += 1
    #print(counter)


    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# if we are not using a video file, stop the camera video stream
#if not args.get("video", False):
 #   vs.stop()

# otherwise, release the camera
#else:
vs.stop()


# close all windows
cv2.destroyAllWindows()
