from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import serial
import time
import statsmodels.api as sm


ball_pts = deque(maxlen=30)
slope_average = deque(maxlen=50)
counter = 0
(dx, dy) = (0, 0)
threshold = 100
top_gutter = 60
bottom_gutter = 420
target_zone = 500
current_position_pixels = 0
number_of_steps = 0
rest_position = 200
response = ''
ball_radius = 0
target_radius = 0
command = 0

#arduino = serial.Serial('COM4',9600)
time.sleep(2)

def nothing(x):
    pass

















cv2.namedWindow("Ball Tracking")
cv2.createTrackbar("LH", "Ball Tracking", 104, 255, nothing)
cv2.createTrackbar("LS", "Ball Tracking", 84, 255, nothing)
cv2.createTrackbar("LV", "Ball Tracking", 122, 255, nothing)
cv2.createTrackbar("UH", "Ball Tracking", 196, 255, nothing)
cv2.createTrackbar("US", "Ball Tracking", 149, 255, nothing)
cv2.createTrackbar("UV", "Ball Tracking", 177, 255, nothing)



cv2.namedWindow("Target Tracking")
cv2.createTrackbar("LH", "Target Tracking", 25, 255, nothing)
cv2.createTrackbar("LS", "Target Tracking", 74, 255, nothing)
cv2.createTrackbar("LV", "Target Tracking", 59, 255, nothing)
cv2.createTrackbar("UH", "Target Tracking", 42, 255, nothing)
cv2.createTrackbar("US", "Target Tracking", 123, 255, nothing)
cv2.createTrackbar("UV", "Target Tracking", 103, 255, nothing)








# list of tracked points

#pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam

vs = VideoStream(src=0).start()
time.sleep(1)

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
    frame = cv2.line(frame, (0, 200), (target_zone, 200), (0, 0, 255), 2, 8, 0)






    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break


    blurred = cv2.GaussianBlur(frame, (41, 41), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    ball_l_h = cv2.getTrackbarPos("LH", "Ball Tracking")
    ball_l_s = cv2.getTrackbarPos("LS", "Ball Tracking")
    ball_l_v = cv2.getTrackbarPos("LV", "Ball Tracking")
    ball_u_h = cv2.getTrackbarPos("UH", "Ball Tracking")
    ball_u_s = cv2.getTrackbarPos("US", "Ball Tracking")
    ball_u_v = cv2.getTrackbarPos("UV", "Ball Tracking")

    ball_l_b = np.array([ball_l_h, ball_l_s, ball_l_v])
    ball_u_b = np.array([ball_u_h, ball_u_s, ball_u_v])

    target_l_h = cv2.getTrackbarPos("LH", "Target Tracking")
    target_l_s = cv2.getTrackbarPos("LS", "Target Tracking")
    target_l_v = cv2.getTrackbarPos("LV", "Target Tracking")
    target_u_h = cv2.getTrackbarPos("UH", "Target Tracking")
    target_u_s = cv2.getTrackbarPos("US", "Target Tracking")
    target_u_v = cv2.getTrackbarPos("UV", "Target Tracking")

    target_l_b = np.array([target_l_h, target_l_s, target_l_v])
    target_u_b = np.array([target_u_h, target_u_s, target_u_v])



    #Make a mask for the target AND ball?

    ball_mask = cv2.inRange(hsv, ball_l_b, ball_u_b)
    ball_mask = cv2.erode(ball_mask, None, iterations=2)
    ball_mask = cv2.dilate(ball_mask, None, iterations=2)

    cv2.imshow("Ball Tracking",ball_mask)

    target_mask = cv2.inRange(hsv, target_l_b, target_u_b)
    target_mask = cv2.erode(target_mask, None, iterations=2)
    target_mask = cv2.dilate(target_mask, None, iterations=2)

    cv2.imshow("Target Tracking", target_mask)

    ball_cnts = cv2.findContours(ball_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ball_cnts = imutils.grab_contours(ball_cnts)
    ball_center = None

    target_cnts = cv2.findContours(target_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    target_cnts = imutils.grab_contours(target_cnts)
    #target_center = None




    # only proceed if at least one contour was found
    if len(ball_cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        ball_c = max(ball_cnts, key=cv2.contourArea)

        ((ball_x, ball_y), ball_radius) = cv2.minEnclosingCircle(ball_c)
        M = cv2.moments(ball_c)
        ball_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    if len(target_cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        target_c = max(target_cnts, key=cv2.contourArea)

        ((target_x, target_y), target_radius) = cv2.minEnclosingCircle(target_c)
        M = cv2.moments(target_c)
        target_center = (target_zone, int(M["m01"] / M["m00"]))

    print(target_center)



    if ball_radius > 10:
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
        cv2.circle(frame, (int(ball_x), int(ball_y)), int(ball_radius),(0, 255, 0) , 2)
        cv2.circle(frame, ball_center, 5, (0, 0, 255), -1)
        # update the points queue
    ball_pts.appendleft(ball_center)

    previous_ball_position = 0
    # loop over the set of tracked points
    for i in np.arange(1, len(ball_pts)):
        # if either of the tracked points are None, ignore
        # them
        if ball_pts[i - 1] is None or ball_pts[i] is None:
            continue

        # check to see if enough points have been accumulated in
        # the buffer
        if counter >= 20 and i == 1 and ball_pts[-10] is not None:

            dx = ball_pts[-10][0] - ball_pts[i][0]
            dy = ball_pts[-10][1] - ball_pts[i][1]
            pts1 = np.transpose(ball_pts)
            x1 = pts1[0]
            y1 = pts1[1]
            X = sm.add_constant(x1)
            model = sm.OLS(y1, X)
            results = model.fit()

            if dx == 0 or dx > 0 or ball_center[0] < threshold or ball_center[1] > bottom_gutter or ball_center[1] < top_gutter or \
                    ball_center[0] > target_zone:
                continue
            else:
                # slope = dy / dx
                slope = results.params[1]

                # This should help remove some of the outlier values by using the average of the last 30 measurements

                slope_average.appendleft(slope)
                smoothed_slope = np.mean(slope_average)
                projected_target = int(smoothed_slope * (target_zone - ball_center[0]) + ball_center[1]) #This is the projected target!

                if projected_target < top_gutter or projected_target > bottom_gutter:
                    continue

                else:
                    frame = cv2.line(frame, ball_center, (target_zone, projected_target), (0, 0, 255), 3, 8, 0)

                    cv2.circle(frame, (target_zone, projected_target), 5, (255, 0, 255), -1)

                    #Determine if the hole is BELOW, ABOVE, OR EQUAL to the projected target
                    #Only send if the command is different


                    if (projected_target > 200) and command != 1:
                        command = 1
                        print("MOVE UP")


                    elif (projected_target < target_center[1]) and command != 2:
                        command = 2
                        print("MOVE DOWN")

                    elif (projected_target == target_center[1]):
                        command = 0
                        print("STOP")


                    # arduino.write((str(projected_target) + '\n').encode())

















    # show the frame to our screen

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    counter += 1



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
