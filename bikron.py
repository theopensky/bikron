#!/usr/bin/env python
# Bikron BCD Binary Clock
# Adapted from online sources
# Version 1.5 October 7, 2020
# Unicorn pHat 8 Columns, 4 Rows
#
#    76543210
#   1********
#   2********
#   4********
#   8********
# Least Common Digit at the top
#
# Optional Displays
#
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
#right Date Column (2 columns)
date_enable = 0
date_col = 5
rd, gd, bd = COLORS['olive']
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
# Temperature Column
temp_enable = 1
temp_col = 6
rt, gt, bt = COLORS['maroon']
# WindSpeed Column
wind_enable = 1
wind_col = 5
rws, gws, bws = COLORS['olive']
# GetWeather Control
weather_enable = 1
refresh = [8, 18, 28, 38, 48, 58] # Weather on the 8's


#background OFF color
rz, gz, bz = COLORS['black']

def GetWeather():
  if weather_enable :
    temp = 52
    wind = 5
    d = {'api_key': 'yourapikey',
         'stationID': 'yourstationid'}

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
  minint = int(time.strftime("%M"))
  if refresh.count(minint):
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

      for y in range(0, 4):
        if binary_list[y] == '1':
          unicorn.set_pixel(x+temp_col,y,rt,gt,bt)
        else:
          unicorn.set_pixel(x+temp_col,y,rz,gz,bz)

  # Calculate and render WindSpeed
    wind = weather[1]
    windd = wind
    if wind > 15 : windd = 15
    wbin = bin(windd) [2:].rjust(4, '0')
    wbin_list = list(wbin)
    for y in range(0, 4):
      if wbin_list[y] == '1':
        unicorn.set_pixel(wind_col,y,rws,gws,bws)
      else:
        unicorn.set_pixel(wind_col,y,rz,gz,bz)

  # Render Month
    if month_enable :
      mobin = bin(int(monthd)) [2:].rjust(4, '0')
      mobin_list = list(mobin)
      for y in range(0, 4):
        if mobin_list[y] == '1':
          unicorn.set_pixel(month_col,y,rmo,gmo,bmo)
        else:
          unicorn.set_pixel(wday_col,y,rz,gz,bz)


  # Render day of week
    if wday_enable :
      wdbin = bin(int(wdayd)+1) [2:].rjust(4, '0')
      wdbin_list = list(wdbin)
      for y in range(0, 4):
        if wdbin_list[y] == '1':
          unicorn.set_pixel(wday_col,y,rw,gw,bw)
        else:
          unicorn.set_pixel(wday_col,y,rz,gz,bz)


  # Render date
    if date_enable :
      for x in range(0, 2):
        binary = bin(int(dated_list[x]))[2:].rjust(4, '0')
        binary_list = list(binary)

        for y in range(0, 4):
          if binary_list[y] == '1':
            unicorn.set_pixel(x+date_col,y,rd,gd,bd)
          else:
            unicorn.set_pixel(x+date_col,y,rz,gz,bz)


  # Render Seconds
    for x in range(0, 2):
      binary = bin(int(secsd_list[x]))[2:].rjust(4, '0')
      binary_list = list(binary)

      for y in range(0, 4):
        if binary_list[y] == '1':
          unicorn.set_pixel(x+secs_col,y,rs,gs,bs)
        else:
          unicorn.set_pixel(x+secs_col,y,rz,gz,bz)

  # Render Minutes
    for x in range(0, 2):
      binary = bin(int(minsd_list[x]))[2:].rjust(4, '0')
      binary_list = list(binary)

      for y in range(0, 4):
        if binary_list[y] == '1':
          unicorn.set_pixel(x+mins_col,y,rm,gm,bm)
        else:
          unicorn.set_pixel(x+mins_col,y,rz,gz,bz)


  #Render Hours
    hbin = bin(int(hourd)) [2:].rjust(4, '0')
    hbin_list = list(hbin)
    for y in range(0, 4):
      if hbin_list[y] == '1':
        unicorn.set_pixel(hours_col,y,rh,gh,bh)
      else:
        unicorn.set_pixel(hours_col,y,rz,gz,bz)

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
#weather = GetWeather() # Get the weather on startup
weather = [52,5] # Internet connection not available on boot?

try:
  loop()
except (KeyboardInterrupt):
  destroy()

