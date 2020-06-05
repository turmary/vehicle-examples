import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
Pin = 33
GPIO.setup(Pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)
while 1 == GPIO.input(Pin):
    pass
print("pressed")
