import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2,GPIO.IN)

switch = GPIO.input(2)

while True:
	if not GPIO.input(2):
		print("press")
		break
