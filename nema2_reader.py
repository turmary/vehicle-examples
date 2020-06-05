#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import pynmea2
import serial

import sys
if len(sys.argv) <= 1:
    print("Usage: %s tty-dev" % sys.argv[0])
    print("          tty-dev a char device as /dev/tty?")
    exit(1)


import RPi.GPIO as GPIO
import time

# J14
PIN_G_STANDY = 36 # MPU_GPS_STANDBY
PIN_G_RST    = 37 # MPU_GPS_RST

def l70r_init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    GPIO.setup(PIN_G_STANDY, GPIO.OUT)
    GPIO.setup(PIN_G_RST, GPIO.OUT)

    GPIO.output(PIN_G_STANDY, GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(PIN_G_RST, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(PIN_G_RST, GPIO.LOW)
    time.sleep(0.01)
    GPIO.output(PIN_G_STANDY, GPIO.LOW)
    time.sleep(0.01)

l70r_init()
ser = serial.Serial(sys.argv[1], 9600, timeout=5.0)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

while 1:
    try:
        line = sio.readline()
        msg = pynmea2.parse(line)
        print(repr(msg))
    except serial.SerialException as e:
        print('Device error: {}'.format(e))
        break
    except pynmea2.ParseError as e:
        print('Parse error: {}'.format(e))
        continue

