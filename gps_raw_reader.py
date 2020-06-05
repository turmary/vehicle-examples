import RPi.GPIO as GPIO
import time
import serial
def InitGPS():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    GPIO.setup(36, GPIO.OUT)  #MPU_GPS_STANDBY
    GPIO.setup(37, GPIO.OUT)  #MPU_GPS_RST

    GPIO.output(36,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(37,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(37,GPIO.LOW)
    time.sleep(1)
    GPIO.output(36,GPIO.HIGH)
    time.sleep(0.1)    
def main():
    InitGPS()
    ser = serial.Serial('/dev/ttyAMA0', 9600)
    while True:
        print(ser.readline())
if __name__ == "__main__":
    main() 