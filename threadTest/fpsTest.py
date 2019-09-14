from __future__ import print_function
from PiVideoStream import PiVideoStream
from FPS import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2

#construct argument parse to parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100, help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=1, help="whether or not to display frames")
args = vars(ap.parse_args())

#init camera and stream
camera = PiCamera()
camera.resolution = (640,480)
#camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
stream = camera.capture_continuous(rawCapture, format = 'bgr', use_video_port = True)

camera.close()

vs = PiVideoStream(resolution=(640,480)).start()
time.sleep(2.0)
fps = FPS().start()

while fps._numFrames < args["num_frames"]:
	#grab frame from threaded video stream and resize it
	frame = vs.read()
	frame = imutils.resize(frame, width=640)

	#check to see if frame should be displayed
	if args["display"] > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

	#update fps counter
	fps.update

#stop timer and display FPS info
fps.stop()
print("[INFO] approx FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
