import sys
import os
from mainGUI import *
from globals import Globals
from time import sleep
import RPi.GPIO as GPIO
import cv2
from picamera import PiCamera
from PIL import Image
from picamera.array import PiRGBArray

camera=PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(22,GPIO.OUT) #A1
GPIO.setup(23,GPIO.OUT) #A2
GPIO.setup(27,GPIO.OUT) #SLP Pin

GPIO.output(27,True)

sleep(0.1)

#def px(x, y):
#	return int(gray[y, x])
#sum = 0
bestFocusVal = 0
whereToFocus = 0
currentStep = 0

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
	#positon motor
	if currentStep >= 1:
		GPIO.output(22,False)
		GPIO.output(23,True)
		tempVar = currentStep-whereToFocus
		sleep(tempVar)
		GPIO.output(23,False)
		currentStep = whereToFocus
		GPIO.output(23,True)
		sleep(whereToFocus)
		GPIO.output(23,False)
		print(whereToFocus)
		print(currentStep)
		break
	currentStep = currentStep + 0.125
	GPIO.output(22,True)
	GPIO.output(23,False)
	sleep(0.125)

	#get numpy array representing image
	image = frame.array
	cv2.imshow("Frame",image)

	#grayscale image to prep for focus testing
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

	focusVal = cv2.Laplacian(image, cv2.CV_64F).var()
	print(focusVal)

	if focusVal >= bestFocusVal:
		bestFocusVal = focusVal
		whereToFocus = currentStep

#	height, width = image.shape[0:2]
#	for x in range(0,width-1,50):
#		for y in range(0,height,50):
#			sum += abs(px(x, y) - px(x+1, y))
#	print(sum)
#	sum = 0

	#clears and gets ready for next string
	rawCapture.truncate(0)

	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		GPIO.output(23,True)
		GPIO.output(22,False)
		sleep(currentStep)
		break

GPIO.output(27,False)
