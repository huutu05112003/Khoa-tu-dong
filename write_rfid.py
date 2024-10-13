from SimpleMFRC522 import SimpleMFRC522
import RPi.GPIO as GPIO
import time
def write_rfid():
	reader = SimpleMFRC522()

	text = input('Type your text: ')
	reader = reader.write(text)
	print('Ghi thanh cong')
	
write_rfid()



