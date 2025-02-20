"""
This script will be practice to understand the most fundamental T/F statements: the button
"""



import RPi.GPIO as GPIO
import time

button = 31	# GPIO pin that the button will read to
led = 37
GPIO.setmode(GPIO.BOARD)

"""
The setup code for the GPIO.IN is crucially important. Because it is an input pin, it will 
read the voltage as binary (3.3V == 1 | 0V == 0). This means that the voltage cannot fluctuate. This 
can be achieved using a "pull up resistor" or a "Pull down resistor". Do not mistake these for virtual or 
digital objects, they are actual circuitry components; it just so happens that because the Pi is equipped
for Mechatronics, they have it so you can configure these pins to connect a pull up/down resistor

Pull up resistor: Default voltage HIGH
Pull down resistor: Default voltage LOW
"""

#GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)	#initializes button pin as an input pin with pull up resistor
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	#initializes button pin as an input pin with pull down resistor
GPIO.setup(led, GPIO.OUT)

try:
	while True:
		buttonState = GPIO.input(button) #stores button state as binary value. "button" is variable that stores button pin number

		if buttonState == GPIO.LOW:
			GPIO.output(led,GPIO.HIGH) #turns LED on
			print("The led is on")
		else:
			GPIO.output(led, GPIO.LOW) #turns LED off
			print("The led is off")
		time.sleep(0.5)                #short loop allows for program to ignore odd fluctuations

except KeyboardInterrupt:
	print("Program stopped by user")

finally:
	GPIO.cleanup()