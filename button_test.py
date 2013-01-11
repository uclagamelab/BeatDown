from time import sleep
import os
import RPi.GPIO as GPIO

BUTTON_PINS = [23, 24, 25, 4]
LED_PINS = [18, 10, 22, 17]

GPIO.setmode(GPIO.BCM)
for i in BUTTON_PINS:
	GPIO.setup(i, GPIO.IN)

for i in LED_PINS:
	GPIO.setup(i, GPIO.OUT)



while True:
	for i in range(4):
		if ( GPIO.input(BUTTON_PINS[i]) == False ):
			print 'b ' + str(i)
			GPIO.output(LED_PINS[i], True)
		else:
			GPIO.output(LED_PINS[i], False)
        sleep(.25);
