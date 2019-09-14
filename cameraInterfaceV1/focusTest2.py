import sys
import os
import RPi.GPIO as GPIO
from time import sleep
import cv2
from picamera import PiCamera
from PIL import Image
from picamera.array import PiRGBArray

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

control_pins = [4,22,17,27] #[A1,A2,B1,B2] respectively

for pin in control_pins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, 0)

camera=PiCamera()
camera.resolution = (640,480)
camera.framerate=32
rawCapture = PiRGBArray(camera, size=(640,480))


halfstep_seq = [
	[1,0,0,0],
	[1,1,0,0],
	[0,1,0,0],
	[0,1,1,0],
	[0,0,1,0],
	[0,0,1,1],
	[0,0,0,1],
	[1,0,0,1]

]

halfstep_reverse_seq = [
	[1,0,0,1],
	[0,0,0,1],
	[0,0,1,1],
	[0,0,1,0],
	[0,1,1,0],
	[0,1,0,0],
	[1,1,0,0],
	[1,0,0,0]
]

stepcount = 0
direction = 1
bestFocusVal = 0
whereToFocus = 0
i = 0

sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

	#get frame from camera and bring into opencv
	if i%10==0:
		image = frame.array
		cv2.imshow("Frame",image)
		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		focusVal = cv2.Laplacian(image, cv2.CV_64F).var()
		print(focusVal)
		if focusVal > bestFocusVal:
			bestFocusVal = focusVal
			whereToFocus = stepcount

	if i <= 120:
		for halfstep in range(8):
			for pin in range(4):
				GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
			sleep(0.0025)
		print(stepcount)
		stepcount = stepcount + 1
		i = i+1
	if i > 120:
		for x in range(120-whereToFocus):
			for halfstep in range(8):
				for pin in range(4):
					GPIO.output(control_pins[pin], halfstep_reverse_seq[halfstep][pin])
				sleep(0.0025)
			print(stepcount)
			stepcount = stepcount - 1
		break
	rawCapture.truncate(0)
	#need waitkey to for imshow
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

camera.start_preview()
#sleep(10)
for x in range(10):
	for halfstep in range(8):
		for pin in range(4):
			GPIO.output(control_pins[pin],halfstep_reverse_seq[halfstep][pin])
			sleep(0.01)
sleep(5)

camera.stop_preview()

for x in range(whereToFocus):
	for halfstep in range(8):
		for pin in range(4):
			GPIO.output(control_pins[pin],halfstep_reverse_seq[halfstep][pin])
			sleep(0.0025)

GPIO.cleanup()
