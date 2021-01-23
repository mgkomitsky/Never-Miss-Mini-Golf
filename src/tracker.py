import cv2
import numpy as np
import imutils
from filterpy.kalman import KalmanFilter

class Tracker():

    def __init__(self):

        self.cap = None
        self.currentFrame = None
        self.windowName = "Trackbars"
        cv2.namedWindow(self.windowName)
        cv2.resizeWindow(self.windowName, 800, 800)
        cv2.namedWindow("Video")
        cv2.namedWindow("Mask")
        # These variables are for the mask

        self.BALL_HSV = [[0, 0, 0], [255, 255, 255]]
        self.TARGET_HSV = [[0, 0, 0], [255, 255, 255]]

        self.f = KalmanFilter(dim_x=2, dim_z=2)

    def nothing(self, x):
        pass

    def drawTrackbars(self):

        cv2.createTrackbar("Ball LH", self.windowName, 0, 255, self.nothing)
        cv2.createTrackbar("Ball LS", self.windowName, 0, 255, self.nothing)
        cv2.createTrackbar("Ball LV", self.windowName, 102, 255, self.nothing)
        cv2.createTrackbar("Ball UH", self.windowName, 255, 255, self.nothing)
        cv2.createTrackbar("Ball US", self.windowName, 172, 255, self.nothing)
        cv2.createTrackbar("Ball UV", self.windowName, 255, 255, self.nothing)

        cv2.createTrackbar("Target LH", self.windowName, 0, 255, self.nothing)
        cv2.createTrackbar("Target LS", self.windowName, 0, 255, self.nothing)
        cv2.createTrackbar("Target LV", self.windowName, 0, 255, self.nothing)
        cv2.createTrackbar("Target UH", self.windowName,
                           255, 255, self.nothing)
        cv2.createTrackbar("Target US", self.windowName,
                           255, 255, self.nothing)
        cv2.createTrackbar("Target UV", self.windowName,
                           255, 255, self.nothing)

    def returnTrackbarPosition(self):
        ball_l_h = cv2.getTrackbarPos("Ball LH", self.windowName)
        ball_l_s = cv2.getTrackbarPos("Ball LS", self.windowName)
        ball_l_v = cv2.getTrackbarPos("Ball LV", self.windowName)
        ball_u_h = cv2.getTrackbarPos("Ball UH", self.windowName)
        ball_u_s = cv2.getTrackbarPos("Ball US", self.windowName)
        ball_u_v = cv2.getTrackbarPos("Ball UV", self.windowName)

        target_l_h = cv2.getTrackbarPos("Target LH", self.windowName)
        target_l_s = cv2.getTrackbarPos("Target LS", self.windowName)
        target_l_v = cv2.getTrackbarPos("Target LV", self.windowName)
        target_u_h = cv2.getTrackbarPos("Target UH", self.windowName)
        target_u_s = cv2.getTrackbarPos("Target US", self.windowName)
        target_u_v = cv2.getTrackbarPos("Target UV", self.windowName)

        self.BALL_HSV = [[ball_l_h, ball_l_s, ball_l_v],
                         [ball_u_h, ball_u_s, ball_u_v]]

        self.TARGET_HSV = [[target_l_h, target_l_s, target_l_v],
                           [target_u_h, target_u_s, target_u_v]]

    def setupVideoStream(self):
        #self.cap = cv2.VideoCapture(0)
        self.cap = cv2.VideoCapture('test2.mkv')

    def showFrame(self):
        cv2.imshow("Video", self.currentFrame)

    def setFrame(self):
        ret, self.currentFrame = self.cap.read()

    def findContours(self, mask):  # Print center of contour
        contours = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        ball_c = max(contours, key=cv2.contourArea)

        ((ball_x, ball_y), ball_radius) = cv2.minEnclosingCircle(ball_c)

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

    def everyFrame(self):  # Run this set of functions for every frame
        self.setFrame()
        self.showFrame()

    def openWindow(self, windowName, l=800, w=800):
        cv2.namedWindow(windowName)
        cv2.resizeWindow(windowName, l, w)