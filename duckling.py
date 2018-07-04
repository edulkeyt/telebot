from __future__ import print_function

#picamera
from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera
import time

#detection
import sys
sys.path.append("/usr/local/lib/python3.5/site-packages")
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

#robot
from wheels import WheelsController

RESOLUTION_WIDTH = 640
RESOLUTION_HEIGHT = 320
FRAMERATE = 32

ROBOT_SCREEN_CENTER_DELTA = 100
ROBOT_SCREEN_CENTER_X = RESOLUTION_WIDTH / 2
# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--images", required=True, help="path to images directory")
#args = vars(ap.parse_args())

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# initialize the camera and grab a reference to the raw camera capture
camera = picamera.PiCamera()
camera.resolution = (RESOLUTION_WIDTH, RESOLUTION_HEIGHT)
camera.framerate = FRAMERATE
rawCapture = PiRGBArray(camera, size=(RESOLUTION_WIDTH, RESOLUTION_HEIGHT))
 
# allow the camera to warmup
time.sleep(0.1)
 
 wheels = WheelsController();
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	image = imutils.resize(image, width=min(400, image.shape[1]))
	orig = image.copy()
 
	# detect people in the image
	(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
		padding=(8, 8), scale=1.05)
 
	# draw the original bounding boxes
	for (x, y, w, h) in rects:
		cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
	# apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
 
	# draw the final bounding boxes
	for (xA, yA, xB, yB) in pick:
		cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
 
	# show the output images
	#cv2.imshow("Before NMS", orig)
	cv2.imshow("After NMS", image)
	#cv2.waitKey(0)
	
	if len(pick) > 0:
		target = pick[0];
		targetX = (target.xB - target.xA) / 2	
		if targetX < ROBOT_SCREEN_CENTER_X - ROBOT_SCREEN_CENTER_DELTA:
			#left
			wheels.setWheelsStateFromStrings(["5","0","200"])
		elif targetX > ROBOT_SCREEN_CENTER_X + ROBOT_SCREEN_CENTER_DELTA:
			#right
			wheels.setWheelsStateFromStrings(["5","200","0"])
		else:
			#forward
			wheels.setWheelsStateFromStrings(["5","220","0"])
	else:
		#stop
		wheels.setWheelsStateFromStrings(["0","0","0"])
		
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break