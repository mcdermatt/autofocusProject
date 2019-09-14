from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2

class FaceTrack:
	def __init__(self, frame, face_cascade):
		x = 0
		y = 0
		w = 0
		h = 0
		face_cascade = cv2.CascadeClassifier('/home/pi/haarcascade_frontalface_default.xml')

#		self.frame = None
		self.stopped = False

	def start(self):
		Thread(target=self.update, args=()).start
		return self

#	def recieve(self, frame):
#		self.frame = frame

	def update(self, frame, face_cascade):
		while True:
			self.frame = frame
			gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			faces = face_cascade.detectMultiScale(gray, 1.1, 5)
			if self.stopped:
				return

	def stop(self):
		self.stopped = True
