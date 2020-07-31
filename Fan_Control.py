#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
if len(sys.argv) <= 1:
    print("Usage: %s on/off" % sys.argv[0])
    exit(1)
class FAN:
    def __init__(self):
        self.Path = '/sys/devices/pwm-fan/target_pwm'
        try:
            self.f = open(self.Path, 'w')
        except IOError as err:
            os.system('sudo chmod 777 %s'%self.Path)
            self.f = open(self.Path, 'w')        
    def power_on(self):
        self.f.write('255')
        self.f.flush()
    def power_off(self):
        self.f.write('0')
        self.f.flush()
def main():
    Fan = FAN()
    if sys.argv[1] == "on":
        Fan.power_on()
        print("power on Fan")
    if sys.argv[1] == "off":
        Fan.power_off()
        print("power off Fan")
if __name__ == "__main__":
    main()