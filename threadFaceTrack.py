from time import sleep
import threading
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

def find_face(self, image):
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.1, 5)
	sleep(0.1)

def update_frame(self):
#		image = frame.array
	if len(faces) > 0:
		for (x,y,w,h) in faces:
			cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),6)
#	add = cv2.addWeighted(image, 0.6, overlay, 0.4, 0)
	cv2.imshow("Frame", image)
	rawCapture.truncate(0)

camera = PiCamera()
camera.resolution = (640,480)
rawCapture = PiRGBArray(camera, size=(640,480))

sleep(0.1)

face_cascade = cv2.CascadeClassifier('/home/pi/haarcascade_frontalface_default.xml')

x = 0
y = 0
w = 0
h = 0

overlay = cv2.imread('overlay.png')
#overlay = cv2.resize(overlay, (480, 320))
key = cv2.waitKey(1) & 0xFF

for frame in camera.capture_continuous(rawCapture, format = 'bgr', use_video_port = True):

	image = frame.array
	t1=threading.Thread(target=find_face, args=(image,))
	t1.start()
	t1.join()

	t2=threading.Thread(target=update_frame, args=(faces,))
	t2.start()
	t2.join()

#	t1.start(image)
#	t2.start(faces)

#	t1.join()
#	t2.join()

	if key == ord("q"):
		break
