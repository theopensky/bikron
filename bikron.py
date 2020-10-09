#!/usr/bin/env python
# Bikron BCD Binary Clock
# Adapted from online sources
# Version 1.71 October 9, 2020
# Unicorn pHat 8 Columns, 4 Rows
#
# Optional Displays
#  LSD - top or bottom
#  Day of week 1-7 (Sunday - Saturday)
#  Month 1-12
#  Day of month - Tens - 0-3
#  Day of month - Ones - 0-9
#  Temperature - 00-99
#  Wind Speed - 0-15
#
#  Not optional:
#  Hours 1-12
#  Minutes - Tens - 0-5
#  Minutes - Ones - 0-9
#  Seconds - Tens - 0-5
#  Seconds - Ones - 0-9

import unicornhat as unicorn
import time
import colorsys
import math
import os.path
import json
from urllib3 import PoolManager

unicorn.set_layout(unicorn.PHAT)
unicorn.brightness(0.5)
unicorn.rotation(0)
width,height=unicorn.get_shape()

COLORS = {
    'red':(255,0,0),
    'lime':(0,255,0),
    'blue':(0,0,255),
    'yellow':(255,255,0),
    'magenta':(255,0,255),
    'cyan':(0,255,255),
    'black':(0,0,0),
    'ltgray':(96,96,96),
    'white':(255,255,255),
    'gray':(127,127,127),
    'grey':(127,127,127),
    'silver':(192,192,192),
    'maroon':(128,0,0),
    'olive':(128,128,0),
    'green':(0,128,0),
    'purple':(128,0,128),
    'teal':(0,128,128),
    'navy':(0,0,128),
    'orange':(255,165,0),
    'gold':(255,215,0),
    'purple':(128,0,128),
    'indigo':(75,0,130)
}
# Columns are numbered 76543210 left to right

#Hours Column (1 column)
hours_col = 4
rh, gh, bh = COLORS['green']
#right Minutes Column (2 columns)
mins_col = 2
rm, gm, bm = COLORS['teal']
#right Seconds Column (2 columns)
secs_col = 0
rs, gs, bs = COLORS['purple']
#Weekday (1 column)
wday_enable = 0
wday_col = 7
rw, gw, bw = COLORS['maroon']
#Month (1 column)
month_enable = 0
month_col = 7
rmo, gmo, bmo = COLORS['maroon']
#right Date Column (2 columns)
date_enable = 0
date_col = 5
rd, gd, bd = COLORS['olive']
#right Temperature Column (2 columns)
temp_enable = 1
temp_col = 6
rt, gt, bt = COLORS['maroon']
# WindSpeed Column (1 column)
wind_enable = 1
wind_col = 5
rws, gws, bws = COLORS['olive']
#background OFF color
rz, gz, bz = COLORS['black']
# GetWeather Control
weather_enable = 1
refresh = [8, 18, 28, 38, 48, 58] # Weather on the 8's

# Least Significant Digit at the top?: true or false
LSD = 1

# Perform the flip:
if LSD == 0 :
  unicorn.rotation(180)

# Load the weather with an X until it's updated
# And delay the first update by at least one minute
weather = [52,5]
weather_delay = 3

def GetWeather():
  temp = 52
  wind = 5
  if weather_enable :
    d = {'api_key': 'yourapikey',
         'stationID': 'yourstationID'}

    pm = PoolManager()
    try:
      r = pm.request('GET','https://api.weather.com/v2/pws/observations/current?stationId=' + d['stationID'] + '&format=json&units=e&apiKey=' + d['api_key'])

      obs = json.loads(r.data.decode('utf-8'))
      temp = obs['observations'][0]['imperial']['temp']
      wind = obs['observations'][0]['imperial']['windSpeed']
    except MaxRetryError as ex:
      temp = 52
      wind = 5

  mylist = [temp, wind]
  return mylist


def isalarm(ah, am):
  alarmfound = 0
  filepath = '/home/pi/Bikron/alarms.txt'
  if os.path.exists(filepath) :
    with open(filepath) as fi:
      line = fi.readline()
      while line:
        if (line.find('#') == 0) :
          line = fi.readline() # ignore comment line
        if (line.find(':') > 0) :
          (hr, mn) = line.split(':')
          mn = mn[0:2]         # strip anything past two digits
          if ((int(hr) == ah) & (int(mn) == am)) :
            alarmfound = 1
        line = fi.readline()

    fi.close()
  return alarmfound

def rainbow(rminute):
 # This function will execute for one minute
  minint = int(time.strftime("%M"))
  i = 0.0
  offset = 30
  while (minint == rminute):
        minint = int(time.strftime("%M"))
        i = i + 0.3
        for y in range(height):
                for x in range(width):
                        r = 0
                        g = 0
                        r = (math.cos((x+i)/2.0) + math.cos((y+i)/2.0)) * 64.0 + 128.0
                        g = (math.sin((x+i)/1.5) + math.sin((y+i)/2.0)) * 64.0 + 128.0
                        b = (math.sin((x+i)/2.0) + math.cos((y+i)/1.5)) * 64.0 + 128.0
                        r = max(0, min(255, r + offset))
                        g = max(0, min(255, g + offset))
                        b = max(0, min(255, b + offset))
                        unicorn.set_pixel(x,y,int(r),int(g),int(b))
        unicorn.show()
        time.sleep(0.01)
  unicorn.clear()
#def rainbow

def binclock(bminute):
  # This function will execute for one minute
  global weather
  global weather_delay

  if weather_delay > 0 :
    if weather_delay == 1 :
      weather = GetWeather()  # Get weather on startup after delay
    weather_delay -= 1

  minint = int(time.strftime("%M"))
  if refresh.count(minint) and not weather_delay :
    weather = GetWeather()

  while (bminute == minint):
    minint = int(time.strftime("%M"))
    secsd = time.strftime("%S") [::-1]
    minsd = time.strftime("%M") [::-1]
    hourd = time.strftime("%I")
    dated = time.strftime("%d") [::-1]
    wdayd = time.strftime("%w")
    monthd = time.strftime("%m")
    tempd = ("%02d" % weather[0]) [::-1]
    secsd_list = list(secsd)
    minsd_list = list(minsd)
    dated_list = list(dated)
    tempd_list = list(tempd)

  # Render Temperature
    for x in range(0, 2):
      binary = bin(int(tempd_list[x]))[2:].rjust(4, '0')
      binary_list = list(binary)
      col = x+temp_col if LSD else 7-temp_col-x
      for y in range(0, 4):
        if binary_list[y] == '1':
          unicorn.set_pixel(col,y,rt,gt,bt)
        else:
          unicorn.set_pixel(col,y,rz,gz,bz)

  # Calculate and render WindSpeed
    wind = weather[1]
    windd = wind
    if wind > 15 : windd = 15
    wbin = bin(windd) [2:].rjust(4, '0')
    wbin_list = list(wbin)
    col = wind_col if LSD else 7-wind_col
    for y in range(0, 4):
      if wbin_list[y] == '1':
        unicorn.set_pixel(col,y,rws,gws,bws)
      else:
        unicorn.set_pixel(col,y,rz,gz,bz)

  # Render Month
    if month_enable :
      mobin = bin(int(monthd)) [2:].rjust(4, '0')
      mobin_list = list(mobin)
      col = month_col if LSD else 7-month_col
      for y in range(0, 4):
        if mobin_list[y] == '1':
          unicorn.set_pixel(col,y,rmo,gmo,bmo)
        else:
          unicorn.set_pixel(col,y,rz,gz,bz)


  # Render day of week
    if wday_enable :
      wdbin = bin(int(wdayd)+1) [2:].rjust(4, '0')
      wdbin_list = list(wdbin)
      col = wday_col if LSD else 7-wday_col
      for y in range(0, 4):
        if wdbin_list[y] == '1':
          unicorn.set_pixel(col,y,rw,gw,bw)
        else:
          unicorn.set_pixel(col,y,rz,gz,bz)


  # Render date
    if date_enable :
      for x in range(0, 2):
        binary = bin(int(dated_list[x]))[2:].rjust(4, '0')
        binary_list = list(binary)
        col = x+date_col if LSD else 7-date_col-x
        for y in range(0, 4):
          if binary_list[y] == '1':
            unicorn.set_pixel(col,y,rd,gd,bd)
          else:
            unicorn.set_pixel(col,y,rz,gz,bz)

  # Render Seconds
    for x in range(0, 2):
      binary = bin(int(secsd_list[x]))[2:].rjust(4, '0')
      binary_list = list(binary)
      col = (x+secs_col) if LSD else (7-secs_col-x)
      for y in range(0, 4):
        if binary_list[y] == '1':
          unicorn.set_pixel(col,y,rs,gs,bs)
        else:
          unicorn.set_pixel(col,y,rz,gz,bz)

  # Render Minutes
    for x in range(0, 2):
      binary = bin(int(minsd_list[x]))[2:].rjust(4, '0')
      binary_list = list(binary)
      col = (x+mins_col) if LSD else (7-mins_col-x)
      for y in range(0, 4):
        if binary_list[y] == '1':
          unicorn.set_pixel(col,y,rm,gm,bm)
        else:
          unicorn.set_pixel(col,y,rz,gz,bz)


  #Render Hours
    hbin = bin(int(hourd)) [2:].rjust(4, '0')
    hbin_list = list(hbin)
    col = (hours_col) if LSD else (7-hours_col)
    for y in range(0, 4):
      if hbin_list[y] == '1':
        unicorn.set_pixel(col,y,rh,gh,bh)
      else:
        unicorn.set_pixel(col,y,rz,gz,bz)

    unicorn.show()

#def binclock

# Loop()
# Check for an alarm in the alarms.txt file
# If HR:MM matches, play the rainbow for one minute
# otherwise just run the clock for one minute
# repeat
# To set or delete alarms, simply modify alarms.txt

def loop():

  while 1:
    minint = int(time.strftime("%M"))
    hrsint = int(time.strftime("%H"))
    if isalarm(hrsint, minint):
      rainbow(minint)
    minint = int(time.strftime("%M"))
    binclock(minint)

def destroy():

  unicorn.clear

# Main Program

try:
  loop()
except (KeyboardInterrupt):
  destroy()

