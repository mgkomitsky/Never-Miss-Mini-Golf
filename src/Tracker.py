import cv2
import numpy as np
import imutils
from filterpy.kalman import KalmanFilter
import requests
import json

class Tracker():

    def __init__(self):

        self.cap = None
        self.currentFrame = None
        
        
        cv2.namedWindow("Video", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
       

        cv2.namedWindow("Mask", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
       
       
        # These variables are for the mask

        self.BALL_HSV = [[0, 0, 0], [255, 255, 255]]
        self.TARGET_HSV = [[0, 0, 0], [255, 255, 255]]

        self.f = KalmanFilter(dim_x=2, dim_z=2)
        #Fun comments
    def nothing(self, x):
        pass

    def drawTrackbars(self,window):

        cv2.namedWindow(window)

        cv2.createTrackbar("Ball LH", window, 0, 255, self.nothing)
        cv2.createTrackbar("Ball LS", window, 0, 255, self.nothing)
        cv2.createTrackbar("Ball LV", window, 102, 255, self.nothing)
        cv2.createTrackbar("Ball UH", window, 255, 255, self.nothing)
        cv2.createTrackbar("Ball US", window, 172, 255, self.nothing)
        cv2.createTrackbar("Ball UV", window, 255, 255, self.nothing)

        cv2.createTrackbar("Target LH", window, 0, 255, self.nothing)
        cv2.createTrackbar("Target LS", window, 0, 255, self.nothing)
        cv2.createTrackbar("Target LV", window, 0, 255, self.nothing)
        cv2.createTrackbar("Target UH", window,
                           255, 255, self.nothing)
        cv2.createTrackbar("Target US", window,
                           255, 255, self.nothing)
        cv2.createTrackbar("Target UV", window,
                           255, 255, self.nothing)

    def returnTrackbarPosition(self,window):
        ball_l_h = cv2.getTrackbarPos("Ball LH", window)
        ball_l_s = cv2.getTrackbarPos("Ball LS", window)
        ball_l_v = cv2.getTrackbarPos("Ball LV", window)
        ball_u_h = cv2.getTrackbarPos("Ball UH", window)
        ball_u_s = cv2.getTrackbarPos("Ball US", window)
        ball_u_v = cv2.getTrackbarPos("Ball UV", window)

        target_l_h = cv2.getTrackbarPos("Target LH", window)
        target_l_s = cv2.getTrackbarPos("Target LS", window)
        target_l_v = cv2.getTrackbarPos("Target LV", window)
        target_u_h = cv2.getTrackbarPos("Target UH", window)
        target_u_s = cv2.getTrackbarPos("Target US", window)
        target_u_v = cv2.getTrackbarPos("Target UV", window)

        self.BALL_HSV = [[ball_l_h, ball_l_s, ball_l_v],
                         [ball_u_h, ball_u_s, ball_u_v]]

        self.TARGET_HSV = [[target_l_h, target_l_s, target_l_v],
                           [target_u_h, target_u_s, target_u_v]]

    def setupVideoStream(self, file_name=0):
        self.cap = cv2.VideoCapture(file_name)

    def showFrame(self):
        cv2.imshow("Video", self.currentFrame)

    def setFrame(self):
        ret, self.currentFrame = self.cap.read()

    def findContours(self, mask):  # Print center of contour
        contours = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        contours_map = map(cv2.contourArea,contours)
        # if no contours, return some default value
        if len(contours) > 0:
            ball_c = max(contours, key=cv2.contourArea)

            ((ball_x, ball_y), ball_radius) = cv2.minEnclosingCircle(ball_c)
        else:
            (ball_x, ball_y), ball_radius = (0,0), 10
       
        cv2.circle(self.currentFrame, (int(ball_x), int(ball_y)),
                   int(ball_radius), (0, 255, 0), 2)

    def applyMask(self, frame, lower, upper, window):  # Apply the mask
        FRAME_IN_HSV_SPACE = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(FRAME_IN_HSV_SPACE,
                           np.float32(lower), np.float32(upper))
        cv2.imshow(window, mask)
        return mask

    def fitData(self):  # Create the model
        pass

    def calculateProjectedTarget(self):  # Use model to calculate target
        pass

    def isValid(self):  # Is the projected target a valid point? e.g is it within the target area?
        pass

    def sendCommandToMCU(self):
        pass

    def initializeSerialPort(self):
        pass

    def checkESPState(self):
        #Get json data to set states of the machine
        #response = requests.get("http://52.119.101.179:7980/metrics")
        text = {
	    "ip": "192.168.100.76",
	    "time": "630257",
	    "ssid": "ECEN403-Development",
	    "speed": "0",
	    "mode": "0"}

        response = json.dumps(text)

        print(response)

    def everyFrame(self):  # Run this set of functions for every frame
        self.setFrame()
        self.showFrame()

    def openWindow(self, windowName, l=960, w=540):
        cv2.namedWindow(windowName)
        cv2.resizeWindow(windowName, l, w)