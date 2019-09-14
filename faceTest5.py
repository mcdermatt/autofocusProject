from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from PIL import Image
import threading
from queue import Queue

#init
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

#allow camera time to warm up
time.sleep(0.1)

face_cascade = cv2.CascadeClassifier('/home/pi/haarcascade_frontalface_default.xml')
x = 0
y = 0
w = 0
h = 0

rectangle_lock = threading.Lock()

def exampleJob(worker):



def threader():
	while True:
		worker = q.get()
		exampleJob(worker)
		q.task_done()

q = Queue()

for x in range(2):
	t = threading.Thread(target = threader)
	t.daemon = True
	t.start()

for worker in range(2):
	q.put(worker)

q.join()



#overlay = Image.open('overlay.png')

#capture frames from camera
for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
	#grab the raw numpy array representing the image then init timestamp
	#and occupied/ unoccupied text
	image = frame.array

#	pad = Image.new('RGB', (640,480))
#	pad.paste(overlay, (0,0)

	#facial recognition
	if count%10 == 0:
		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.1, 5)

		if len(faces) > 0:
			for (x,y,w,h) in faces:
				cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),6)


	else:
		cv2.rectangle(image, (x,y), (x+w,y+h),(0,255,255),2)

#	add = image + overlay
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF


	#clear stream to get ready for next one
	rawCapture.truncate(0)
	count = count + 1
	#if q key is pressed, break from loop
	if key == ord("q"):
		break
