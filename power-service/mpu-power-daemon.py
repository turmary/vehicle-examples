#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import os

'''
1.If MCU receive the INT3, it will turn on Mosfet
  to power MPU (Jetson Nano or RPi 4).
2.If the INT3 disappear, the MCU will send INT2 to MPU.
3.If MPU receive the INT2, it will save data.
4.After MPU has saved data , it will send INT1 to
  MCU and  turn off the system.
5.If MCU receive the INT1, it will turn off Mosfet
  after 20 sec
'''
PIN_MCU_INT1 = 29 # Output
PIN_MCU_INT2 = 31 # Input

def power_prepare():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    GPIO.setup(PIN_MCU_INT1,  GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(PIN_MCU_INT2,  GPIO.IN,  pull_up_down = GPIO.PUD_DOWN)

# Without the infrom MPU will be reset by MCU
def inform_startup_end():
    GPIO.output(PIN_MCU_INT1, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(PIN_MCU_INT1, GPIO.LOW)
    time.sleep(0.01)

def wait_signal_int2():
    counter = 0
    while counter < 5:
        if GPIO.input(PIN_MCU_INT2):
            counter += 1
        else:
            counter = 0
        time.sleep(0.01)

def inform_app_to_exit():
    # Write your OWN code
    # To save application DATA
    # then exit, max time 30 seconds.
    time.sleep(5.0)
    return

def system_poweroff():
    GPIO.output(PIN_MCU_INT1, GPIO.HIGH)
    time.sleep(0.1)
    os.system("poweroff")
    return

def main():
    power_prepare()
    inform_startup_end()
    wait_signal_int2()
    inform_app_to_exit()
    system_poweroff()

    while True:
        pass


if __name__ == "__main__":
    main()

