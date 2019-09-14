import pygame
import sys
import os
from mainGUI import *
from globals import Globals
from time import sleep
import RPi.GPIO as GPIO
#import cv2

pygame.init()

scrsize = width,height = 720,480
black = 0,0,0
bgcolor = (255,255,255)
boxcolor = (39,91,178)
txtcolor = (255,255,255)
bgrcolor = (115,135,178)

screen = pygame.display.set_mode(scrsize, pygame.FULLSCREEN)
font = Font.Big

#pygame.mouse.set_visible(False)
screen.fill(bgcolor)
pygame.display.update()

#init GUI----------------

#focus mode button
def focusMenu():
	Globals.scene = "focus"
btnFocus = Menu.Button(text = "Focus Mode", rect = (50,270,160,160),
	bg = boxcolor, fg = txtcolor, bgr = bgrcolor, tag = ("menu", None))
btnFocus.Command = focusMenu

#back button
def goBack():
	Globals.scene = "menu"
btnGoBack = Menu.Button(text = "Back", rect = (20,20,160,80), bg = boxcolor, fg = txtcolor, bgr = bgrcolor, tag = ("focus", None))
btnGoBack.Command = goBack

#set focus to center point
def setCenterPoint():
	Globals.focus_mode = "centerPoint"
	Globals.scene = "menu"
btnSetCenterPoint = Menu.Button(text = "Center Point", rect = (200,60,300,160), bg = boxcolor, fg = txtcolor, bgr = bgrcolor, tag = ("focus", None))
btnSetCenterPoint.Command = setCenterPoint
centerPointThumb = pygame.image.load('/home/pi/cameraInterfaceV1/thumbnails/centerPoint.png')

#set focus to zone
def setZone():
	Globals.focus_mode = "zone"
	Globals.scene = "menu"
btnSetZone = Menu.Button(text = "Zone", rect = (200,260,300,160), bg = boxcolor, fg = txtcolor, bgr = bgrcolor, tag = ("focus", None))
btnSetZone.Command = setZone
zoneThumb = pygame.image.load('/home/pi/cameraInterfaceV1/thumbnails/zone.png')

#motor test
dutyCycle = 95 #0-100 for PWM pin
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(22,GPIO.OUT) #AIN1
GPIO.setup(23,GPIO.OUT)	#AIN2
GPIO.setup(27,GPIO.OUT) #SLP - disable sleep & acivate motor control
#pwm = GPIO.PWM(motorPin, 50) #init PWM on motorPin 100Hz frequency
#pwm.start(dutyCycle)
def moveMotor():
	pygame.draw.rect(screen,(0,255,0),(250,100,50,50)) #indicate pwm on
#	pwm.start(dutyCycle)
	GPIO.output(27, True)
	GPIO.output(22, True)
	GPIO.output(23, False)
	sleep(1)
	GPIO.output(22, False)
	GPIO.output(27, False)
#	pwm.ChangeDutyCycle(100-dutyCycle)
#	sleep(1)
#	pwm.stop() #stop PWM
btnMoveMotor = Menu.Button(text = "Move Motor", rect = (50,50,160,160), bg = boxcolor, fg = txtcolor, bgr = bgrcolor, tag = ("menu", None))
btnMoveMotor.Command = moveMotor

#k = cv2.waitKey(1) & 0xFF #pres q to exit
#main loop ----------------------------------------------
count = 1
while count <= 100:
	if Globals.scene == "menu":
		screen.fill(bgcolor)
		pygame.draw.rect(screen,(211,211,211),(10,240,350,230))
		pygame.draw.rect(screen,(211,211,211),(370,240,340,230))
		pygame.draw.rect(screen,(211,211,211),(10,10,350,220))
		pygame.draw.rect(screen,(211,211,211),(370,10,340,220))
		btnFocus.Render(screen)
		btnMoveMotor.Render(screen)
		if Globals.focus_mode == "centerPoint":
			screen.blit(centerPointThumb, [230,380])
		if Globals.focus_mode == "zone":
			screen.blit(zoneThumb, [230,380])

	if Globals.scene == "focus":
		screen.fill(bgcolor)
		btnSetCenterPoint.Render(screen)
		btnSetZone.Render(screen)
		btnGoBack.Render(screen)

	for event in pygame.event.get():
		if event.type == pygame.MOUSEMOTION:
		#	print (pygame.mouse.get_pos())
			mouse_pos = pygame.mouse.get_pos()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1: #left click
				#process button click event
				for btn in Menu.Button.All:
					if btn.Tag[0] == Globals.scene and btn.Rolling:
						if btn.Command != None:
							btn.Command() #do button event
							btn.Rolling = False
							break #exit loop

	print(mouse_pos)
	pygame.display.update()
	sleep(0.1)
	count = count + 1

pygame.quit()
