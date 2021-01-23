import cv2
import numpy as np
import time
import imutils
from filterpy.kalman import KalmanFilter
from src.tracker import Tracker


track = Tracker()
track.setupVideoStream()
track.drawTrackbars()


while(True):

    track.setFrame()

    time.sleep(.1)
    ball_mask = track.applyMask(track.currentFrame,
                                track.BALL_HSV[0], track.BALL_HSV[1], "Mask")
    track.findContours(ball_mask)
    track.showFrame()
    track.returnTrackbarPosition()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
track.cap.release()
cv2.destroyAllWindows()
