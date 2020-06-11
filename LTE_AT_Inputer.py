#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial
import time
import sys
if len(sys.argv) <= 1:
    print("Usage: %s tty-dev" % sys.argv[0])
    print("          tty-dev a char device as /dev/tty?")
    exit(1)
	# AT+QCFG="band"
	# +QCFG: "band",0x93,0x80800c5,0x0

	# AT+QCFG="nwscanmode"
	# +QCFG: "nwscanmode",0
	# AT+QCFG="nwscanmode",0,1

	# AT+QCFG="nwscanseq"
	# +QCFG: "nwscanseq",0403010205

	# AT+QNWINFO
	# AT+CSQ

	# AT+QIACT?
	# AT+QPING=1,"www.baidu.com"
	# AT+QPING=1,"14.215.177.39"
    
def main():
    ser = serial.Serial(sys.argv[1], 9600, timeout=5.0)
    while True:
        send_data = input("input a data: ")
        send_data = send_data + '\r\n'
        ser.write(send_data.encode())
        data=ser.read(1)
        time.sleep(0.1) 
        data = (data + ser.read(ser.inWaiting())).decode()
        print(data)
if __name__ == "__main__":
    main() 