# SCG Vehicle Device Software Guide

**For Jetson Nano**

**Seeed Technology**

## Specification for SCG Vehicle Device

|Item|Values|
|----|------|
|Peripheral Interface| 1 x USB power for Play<br>1 x Record interface<br>1 x Play interface<br>1 x Vibration Motor interface(MAX 30V/5A)<br>1 x SIM card slot<br>1 x SWD inerface<br>1 x IR_LED interface|
|On-board LED|1 x 3v3 LED<br>1 x MPU_5v LED<br>1 x USER LED<br>1 x 1PPS LED<br>1 x NET_MODE LED<br>1 x NET_STA LED|
|Power|24V/2A|
|Button|1 x USER button<br>1 x Reset button|
|Operating temperature(C) | 0 ~ 60 |

## Hardware Overview

![](./img/hardware_view.png)

- **1. WM8960:** a low power stereo codec.
- **2. Power usb:** Speaker power USB.
- **3. 3.5MM JACK:** 3.5MM JACK for Speaker.
- **4. 3.5MM JACK:** 3.5MM JACK for Mic.
- **5. Led indicter:** report the system information by LED.
- **6. Power switch:** power on / off SCG Vehicle Device.
- **7. Reset button:** Reset SCG Vehicle Device.
- **8. Extern Interface:**  Include 1 x Vibration Motor interface , 1 x 24V power interface , 1 x USER button interface , 1 x IR_LED interface.
- **9. SIM Card slot:** insert SIM card
- **10. EC25-E:** LTE module.
- **11. Temperature sensor:** NPO.
- **12. L70-R:** GPS module.
- **13. LSM6DS3:** 6-DOF Sensor.
- **14. samd21:** power controller.
- **15. SWD interface:** update the firmware to samd21 by use this interface.
- **16. Fan:** Jetson Nano's FAN.
- **17. Grove jack:** connect LTE to Jetson Nano.
- **18. 40PIN:** connect SCG Vehicle Device to Jetson Nano.

## Preparatory Work

**Materials Required**

- SCG Vehicle Device
- Jetson Nano with fan and SD card
- Internet network
- Internet cable
- PC (Windows10)
- [USB To Uart Adapter](https://www.seeedstudio.com/8USB-To-Uart-5V%26amp%3B3V3-p-1832.html) (optional)
- 24V/2A DC interface adapter
- Speaker x 1
- Mic x1
- IR LED x 1
- USB camera x 1

This software provide some shell commands and python script to demo how to drive devices on the SCG Vehicle Device. Most of these `commands` could input to the serial port (setting 115200,8bit,no-parity,no-flow -control) of Jetson Nano or to PUTTY window which connect to Jetson Nano through net/ssh connection.

![](./img/uart_connection.png)

After serial port/putty open, please login with `ubuntu:ubuntu`(User/password).

## Devices Usage

### USB Camera

Connect the USB Camera to any USB port of Jetson Nano.

```bash
# Install cheese application, apt require Internet connection.
sudo apt update
sudo apt install cheese
```

>Note cheese command require GUI output, so it should enter into terminal window of  Ubuntu Desktop, not the serial port or putty window. To input this command, you should use a `USB keyboard & HDMI display`.

```bash
cheese
#Then the video captured by camera will view on HDMI display.
```

### Speaker & Micphone(WM8960)

```bash 
arecord -D hw:1,0 -f S32_LE -r 48000 -c 2 | aplay -D hw:1,0 -f S32_LE -r 48000 -c 2
# The captured sound from jack MICPHONE will playback on jack LOADSPEAKER the same time.
```

If you insert a USB camera before Jetson Nano boot. you must modify the HW option as follows.

```bash
arecord -D hw:2,0 -f S32_LE -r 48000 -c 2 | aplay -D hw:2,0 -f S32_LE -r 48000 -c 2
```

the codec the max sample rates is 48K.the sample rate can be support as follow:
|sample rate|
|:----:|
|8 KHz|
|11.025 KHz|
|12 KHz|
|16 KHz|
|22.05 KHz|
|24 KHz|
|32 KHz|
|44.1 KHz|
|48 KHz|

the more information you can view datasheets that included in the resources package.

>Please try a few more times if it report sound card busy

### Vibration Motor

Download script from:

https://github.com/turmary/vehicle-examples/blob/master/jetson/motor_control.py

>We will always transfer any updates/bugfix to the github repository if required.
```bash
python3 motor_control.py
#Motor on for 2 seconds, then off for 2 seconds, repeatedly.
```

### Button

Download script from:

https://github.com/turmary/vehicle-examples/blob/master/button.py

```bash
python3 button.py
#Wait for user press the BUTTON, echo “pressed” after the press, then exit.
```

### 6-DOF Sensor (LSM6DS3)

```bash
export PYTHONPATH=$HOME/git/LSM6DS3/src
cd $HOME/git/LSM6DS3; python3 examples/example_poll.py
#Display gyroscope & Accelerometer data got by the sensor every 0.3 second.
```

the Sensor the min scale is ±2 g.
the more information you can view datasheets that included in the resources package.

### GPS(L70-R)

Download script from:

https://github.com/turmary/vehicle-examples/blob/master/nema2_reader.py

```bash
#sudo pip3 install pynmea2 pyserial
sudo python3 nema2_reader.py /dev/ttyTHS1
#Display NEMA data got from the GPS module.
```

the more information you can view datasheets that included in the resources package.

### LTE(EC25-E)

>Note insert the SIM card when power off state.

```bash
cd ~/git/linux-ppp-scripts
```

Below setting should consult you SIM-Card/Cell-Network provider.

```bash

# Config User/Password in file quectel
cat quectel
# Config APN in file quectel-chat-connect
cat quectel-chat-connect
# Update the change to system
sudo ./install
```

Download script from:

https://github.com/turmary/vehicle-examples/blob/master/quectel-onoff.py

```bash
# sudo apt install ppp
# Power on the LTE module
sudo python3 quectel-onoff.py
#The USER LED will light when the LTE power successfully.
```

Internet test

```bash
# Dial the Cell Network, run in background
pppd call quectel &
# Test the network
ping -I ppp0 www.china.com
#Should receive response bytes from the site.
```

the more information you can view datasheets that included in the resources package.

### IR_LED

Download script from:

https://github.com/turmary/vehicle-examples/blob/master/IR_Control.py

```bash
#sudo pip3 install smbus
#If you want to power on the IR_LED you can use cmd as follow
sudo python3 IR_Control.py on
#The IR_lED will bright in a dark environment.
#If you want to power off the IR_LED you can use cmd as follow
sudo python3 IR_Control.py off
```

### Fan

Download script from:

https://github.com/Hansen0314/vehicle-examples/blob/master/Fan_Control.py

```bash
#If you want to power on the Fan you can use cmd as follow
sudo python3 Fan_Control.py on
#If you want to power off the Fan you can use cmd as follow
sudo python3 Fan_Control.py off
```

>Since the inertia, the Fan will need some time to stop.
