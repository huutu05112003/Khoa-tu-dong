
import RPi.GPIO as GPIO
khoa_pin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(khoa_pin, GPIO.OUT)
GPIO.setwarnings(False)
import time

	
GPIO.output(khoa_pin, GPIO.HIGH)
	
