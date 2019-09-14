import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

control_pins = [4,22,17,27] #[A1,A2,B1,B2] respectively

for pin in control_pins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, 0)

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

for i in range(100):
	for halfstep in range(8):
		for pin in range(4):
			GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
		sleep(0.0025)
	print(stepcount)
	stepcount = stepcount + 1

for i in range(100):
	for halfstep in range(8):
		for pin in range(4):
			GPIO.output(control_pins[pin], halfstep_reverse_seq[halfstep][pin])
		sleep(0.0025)
	print(stepcount)
	stepcount = stepcount - 1



GPIO.cleanup()
