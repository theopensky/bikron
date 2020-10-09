## **Bikron Binary clock for Raspberry Pi Zero W and Pimoroni Unicorn pHat 8x4 LED Display**

This is a simple binary-coded-decimal clock program for the Unicorn pHat display. The least-common-digit is at the top of the display in a style created by John Wells of Media House Corporation in the 1970's. The basic Bikron clock is 5 columns of 4 lights with the columns being hours (1-12), tens of minutes (0-5), ones of minutes (0-9), tens of seconds (0-5), and ones of seconds (0-9). There are a total of 18 lights with a maximum of 13 lit at any one time (7:57:57 for example). This is important only for calculating voltage and current requirements for clocks made with discrete LED's or other types of light bulbs. 

This clock makes use of the first three extra columns by giving you options to display the day of week, month, date, or weather information from Wunderground.

This clock will also read a text file with 'alarms' entered as HH:MM where the clock will display a colorful pattern for one minute when the alarm time is matched. 

### **Project Instructions**

This project uses a Raspberry Pi Zero W and a Unicorn pHAT. The PiZero uses NTP to set the PI clock so internet connectivity is required.
* Install the Raspbian Lite image on a SD Card and boot on the Pi Zero.
* Configure your Wifi and Timezone settings when prompted.
* Turn on SSH for remote access.
* Update the operating system: ```sudo apt update && sudo apt upgrade -y```
* Install the pHAT libraries: ```curl -sS get.pimoroni.com/unicornhat | bash```
* Grab a copy of the clock program: ```wget https://raw.githubusercontent.com/theopensky/bikron/master/bikron.py```
* Grab a copy of the alarms.txt file or make one yourself (resides in /home/pi/Bikron/alarms.txt)
* Make the clock program executable: ```sudo chmod +x bikron.py```
* Create a crontab to start the clock on bootup: ```sudo crontab -e```
```
     @reboot sudo python3 /home/pi/bikron.py
     0 4 * * * sudo /sbin/reboot now
```
##### The 4AM reboot is just to keep things running smoothly.

