#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Control Vibration Motor through GPIO
#
import RPi.GPIO as GPIO
import time
import sys

# J14 pin 32
PIN_MOTOR = 32

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(PIN_MOTOR, GPIO.OUT)

def main():
    while True:
        GPIO.output(PIN_MOTOR, GPIO.HIGH)
        time.sleep(2.0)
        GPIO.output(PIN_MOTOR, GPIO.LOW)
        time.sleep(2.0)

if __name__ == "__main__":
    main()

