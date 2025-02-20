"""
This script is just to illustrate the use of RPi.gpio module

Follow the comments closely to understand how to interact with a Raspberry Pi

This will blink an LED on and off with a specified pin of 37
"""

import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD) #this command will set the numbering system to board numbering

led = 37 #this is just to store the pin number as a recognizable variable
gpio.setup(led, gpio.OUT) #this sets the pin number "led" as an output pin

try:        #This just tells python to attempt to execute the code in the try block
    while True:     #Just to operate with little to no input. This application is purely for demonstration
        gpio.output(led, gpio.HIGH) #sets the specified pin voltage to HIGH (3.3V on pi) assuming it is set up as output
        time.sleep(1)               #This just sleeps the system for 1 second
        gpio.output(led, gpio.LOW)  #Sets the specified pin to low (meaning 0V)
        time.sleep(1)
finally:
    """
    This is crucial in any gpio application. It will reset the gpio pin settings
    so that further specifications can be made after the execution of the code.
    
    This would not be necessary if the physical configuration never changes, but is still good practice.
    This command will be used upon the GUI termination for the project
    """
    gpio.cleanup()