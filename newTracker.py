import cv2
import numpy as np


class Tracker():

    def __init__(self):

        self.cap = None
        self.currentFrame = None
        self.windowName = "Trackbars"
        cv2.namedWindow(self.windowName)
        cv2.resizeWindow(self.windowName, 800, 800)
        cv2.namedWindow("Video")
        cv2.namedWindow("mask")
        # These variables are for the mask

        self.BALL_HSV = [[0, 0, 0], [255, 255, 255]]
        self.TARGET_HSV = [[0, 0, 0], [255, 255, 255]]

    def nothing(self, x):
        pass

    def drawTrackbars(self):

        cv2.createTrackbar("Ball LH", self.windowName, 0, 255, self.nothing)
        cv2.createTrackbar("Ball LS", self.windowName, 0, 255, self.nothing)
        cv2.createTrackbar("Ball LV", self.windowName, 0, 255, self.nothing)
        cv2.createTrackbar("Ball UH", self.windowName, 255, 255, self.nothing)
        cv2.createTrackbar("Ball US", self.windowName, 255, 255, self.nothing)
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
        self.cap = cv2.VideoCapture(0)

    def showFrame(self):
        cv2.imshow("Video", self.currentFrame)

    def setFrame(self):
        ret, self.currentFrame = self.cap.read()

    def trackObject(self, color):
        pass

    def applyMask(self, frame, lower, upper, window):  # Apply the mask
        FRAME_IN_HSV_SPACE = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(FRAME_IN_HSV_SPACE,
                           np.float32(lower), np.float32(upper))
        cv2.imshow(window, mask)

    def getObjectCoordinates(self):  # Get the coordinates of the object
        pass

    def drawCircleAroundBall(self):
        pass

    def fitData(self):
        pass

    def calculateProjectedTarget(self):
        pass

    def isValid(self):
        pass

    def sendCommandToMCU(self):
        pass

    def everyFrame(self):  # Run this set of functions for every frame
        self.setFrame()
        self.showFrame()


track = Tracker()
track.setupVideoStream()
track.drawTrackbars()


while(True):

    track.everyFrame()

    track.returnTrackbarPosition()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
track.cap.release()
cv2.destroyAllWindows()
