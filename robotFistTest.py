from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from PIL import Image

#init
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

#allow camera time to warm up
time.sleep(0.1)

fist_cascade = cv2.CascadeClassifier('/home/pi/haarCascades/fist_v3.xml')
palm_cascade = cv2.CascadeClassifier('/home/pi/haarCascades/palm_v4.xml')

count = 1
x = 0
y = 0
w = 0
h = 0
a = 0
b = 0
c = 0
d = 0

#overlay = cv2.imread('overlay.png')
#overlay = cv2.resize(overlay, (640,480))

font = cv2.FONT_HERSHEY_SIMPLEX
status = ""

#capture frames from camera
for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
	#grab the raw numpy array representing the image then init timestamp
	#and occupied/ unoccupied text
	image = frame.array

#	pad = Image.new('RGB', (640,480))
#	pad.paste(overlay, (0,0)

	#gesture recognition
	if count%10 == 0:
		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		fists = fist_cascade.detectMultiScale(gray, 1.05, 5)
		palms = palm_cascade.detectMultiScale(gray, 1.1, 5)

		if len(fists) > 0:
			for (x,y,w,h) in fists:
				cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),6)
			status = "fist"
		if len(palms) > 0:
			for (a,b,c,d) in palms:
				cv2.rectangle(image,(a,b),(a+c,b+d),(0,0,255),6)
			status = "palm"

		else:
			w = 0
			h = 0
			x = 0
			y = 0
			a = 0
			b = 0
			c = 0
			d = 0
#			status = " "

	else:
		cv2.rectangle(image, (x,y), (x+w,y+h),(0,255,255),2)
		cv2.rectangle(image, (a,b), (a+c,b+d),(0,0,255),2)
#	add = image + overlay
#	add = cv2.addWeighted(image, 0.6, overlay, 0.4, 0)
	cv2.putText(image,status,(100,100),font,4,(0,0,0),5,cv2.LINE_AA)
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF


	#clear stream to get ready for next one
	rawCapture.truncate(0)
	count = count + 1
	#if q key is pressed, break from loop
	if key == ord("q"):
		break
