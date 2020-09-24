Bikron Binary clock for Raspberry Pi Zero W
and Pimoroni Unicorn pHat 8x4 LED Display

This is a simple binary-coded-decimal clock program for the Unicorn pHat display.
The least-common-digit is at the top of the display in a style created by John Wells of Media House Corporation in the 1970's.
The basic Bikron clock is 5 columns of 4 lights with the columns being hours (1-12), tens of minutes (0-5),
ones of minutes (0-9), tens of seconds (0-5), and ones of seconds (0-9). There are a total of 18 lights with a maximum of 13
lit at any one time (7:57:57 for example). This is important only for calculating voltage and current requirements for clocks made
with discrete LED's or other types of light bulbs. 

This clock makes use of the first three extra columns by displaying the day of week and day of month.

#    7  65  4  32  10
#    _  __  _  __  __
# 1 |*||**||*||**||**|
# 2 |*||**||*||**||**|
# 4 |*||**||*||**||**|
# 8 |*||**||*||**||**|
#    -  --  -  --  --
# Least Common Digit at the top
#
# 7 - Day of week 1-7 (Sunday - Saturday)
# 6 - Day of month - Tens - 0-3
# 5 - Day of month - Ones - 0-9
# 4 - Hours 1-12
# 3 - Minutes - Tens - 0-5
# 2 - Minutes - Ones - 0-9
# 1 - Seconds - Tens - 0-5
# 0 - Seconds - Ones - 0-9

This clock will also read a text file with 'alarms' entered as HH:MM where the clock will display
a colorful pattern for one minute when the alarm time is matched. 

Project Instructions

This project uses a Raspberry Pi Zero W and a Unicorn pHAT. the PiZero uses NTP to set the PI clock so internet connectivity
is required. 
Install the Raspbian Lite image on a SD Card and boot on the Pi Zero.
Configure your Wifi and Timezone settings when prompted.
Turn on SSH for remote access.
Update the operating system:
 sudo apt-get update && sudo apt-get upgrade -y
Install the pHAT libraries:
 curl -sS get.pimoroni.com/unicornhat | bash
Grab a copy of the clock program:
 wget https://raw.githubusercontent.com/theopensky/bikron/master/bikron.py
Grab a copy of the alarms.txt file or make one yourself
Make the clock program executable:
 sudo chmod +x bikron.py
Create a crontab to start the clock on bootup:
 sudo crontab -e
 @reboot sudo python3 /home/pi/bikron.py
 0 4 * * * sudo /sbin/reboot now

The 4AM reboot is just to keep things running smoothly.
