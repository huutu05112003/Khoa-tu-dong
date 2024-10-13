from SimpleMFRC522 import SimpleMFRC522
import RPi.GPIO as GPIO
import time
def read_rfid_card():
	read_test = SimpleMFRC522()
	id, text = read_test.read()
	
	return id, text


