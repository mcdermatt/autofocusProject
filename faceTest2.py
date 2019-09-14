import io
import picamera
import cv2
import numpy
import time
from PIL import Image

#create memory stream
stream=io.BytesIO()
count = 1

#get low resolution picture
with picamera.PiCamera() as camera:
	camera.resolution = (720,480)
#	camera.capture(stream, format='jpeg')
	camera.start_preview()

	#load in image for preview overlay
	img=Image.open('/home/pi/overlay.png')
#	img2=Image.open('/home/pi/overlayRED.png')
	#create image padded to required size
	pad = Image.new('RGB', (
		((img.size[0] + 31) // 32) * 32,
		((img.size[1] +15) // 16) * 16,
		))
#	pad2 = Image.new('RGB', (
#		((img2.size[0] + 31) // 32) * 32,
#		((img2.size[1] +15) // 16) * 16,
#		))
	#paste OG on Pad
	pad.paste(img, (0,0))
#	pad2.paste(img2,(0,0))
	#add overlay
	o = camera.add_overlay(pad.tobytes(), size=img.size)
	o.alpha=128
	o.layer=3
#	a = numpy.zeros((480,720,3), dtype=numpy.uint8)
#	o2 = camera.add_overlay(pad2.tobytes(), size=img2.size)
#	o2.alpha=128
#	o2.layer=1


	while count <= 50:

		#capture image
		camera.capture(stream, format='jpeg')

		#convert the picture to numpy array
		buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

		#create opencv image
		image = cv2.imdecode(buff, 1)

		#load cascade file
		face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')

		#convert to grayscale
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		#look for faces in the image using loaded cascade file
		faces = face_cascade.detectMultiScale(gray, 1.1, 5)

#		print "Found " + str(len(faces))+" faces"

		time.sleep(2)

#		newShit = numpy.asmatrix(stream,dtype=numpy.uint8)
#	o.layer=1
#	o2 = camera.add_overlay(pad2.tobytes(), size=img2.size)
#	o2.alpha=128
#	o2.layer=4
#	time.sleep(2)
	#draw rectangle
		for (x,y,w,h) in faces:
			pad.paste(img,(x,y))
#			o.layer=2
#			a = numpy.zeros((480,720,3), dtype=numpy.uint8)
#			cv2.rectangle(newShit,(x,y),(x+w,y+h),(255,255,0),2)
			oNew = camera.add_overlay(pad.tobytes(),format='rgb', layer=3, alpha=64)

		time.sleep(0.25)
		count = count + 1
#	cv2.imwrite('result.jpg',image)

	camera.stop_preview()
	cv2.destroyAllWindows()
