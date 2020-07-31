#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import smbus
import time
import sys
IR_ADDR = 0X04
POWER_IR_REG = 0X04
POWER_ON_IR = 0X01
POWER_OFF_IR = 0X00
if len(sys.argv) <= 1:
    print("Usage: %s on/off" % sys.argv[0])
    exit(1)
class IR:
    def __init__(self, address):
        self.bus = smbus.SMBus(1)
        self.address = address
    def power_on(self):
        self.bus.write_byte_data(self.address, POWER_IR_REG, POWER_ON_IR)
    def power_off(self):
        self.bus.write_byte_data(self.address, POWER_IR_REG, POWER_OFF_IR)
def main():
    Ir_ring = IR(IR_ADDR)
    if sys.argv[1] == "on":
        Ir_ring.power_on()
        print("power on Ir")
    if sys.argv[1] == "off":
        Ir_ring.power_off()
        print("power off Ir")
if __name__ == "__main__":
    main() 