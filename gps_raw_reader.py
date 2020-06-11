#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import serial
import sys
if len(sys.argv) <= 1:
    print("Usage: %s tty-dev" % sys.argv[0])
    print("          tty-dev a char device as /dev/tty?")
    exit(1)
# J14
PIN_G_STANDY = 36 # MPU_GPS_STANDBY
PIN_G_RST    = 37 # MPU_GPS_RST
def InitGPS():
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
def main():
    InitGPS()
    ser = serial.Serial(sys.argv[1], 9600, timeout=5.0)
    while True:
        print(ser.readline())
if __name__ == "__main__":
    main() 