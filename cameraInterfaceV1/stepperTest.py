import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(22,GPIO.OUT) #A1
GPIO.setup(23,GPIO.OUT) #A2
GPIO.setup(27,GPIO.OUT) #SLP Pin

GPIO.output(27,True)

sleep(0.5)

GPIO.output(23,True)
GPIO.output(22,False)

sleep(0.5)
GPIO.output(23,False)
GPIO.output(22,True)

GPIO.output(27,False)
