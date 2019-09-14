import io
import picamera
import cv2
import numpy

#create memory stream
stream=io.BytesIO()

#get low resolution picture
with picamera.PiCamera() as camera:
	camera.resolution = (320,240)
	camera.capture(stream, format='jpeg')
	camera.start_preview()

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

	print ("Found " + str(len(faces))+" faces")

	#draw rectangle
	for (x,y,w,h) in faces:
		cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)

	cv2.imwrite('result.jpg',image)

	cv2.imshow('image',image)
	cv2.waitKey(33)
	camera.stop_preview()
	cv2.destroyAllWindows()
