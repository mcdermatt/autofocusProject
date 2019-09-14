from threading import Thread
import cv2

class WebcamVideoStream:
	def __init__(self, scr=0)
		#init camera and read first frame from stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()

		#init variable for indicating thread should be stopped
		self.stopped = False

	def start(self):
		thread(target=self.update, args=()).start()
		return self

	def update(self):
		while True:
			if self.stopped:
				return
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		return self.frame

	def stop(self):
		self.stopped = True
