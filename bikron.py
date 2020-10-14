#!/usr/bin/env python
# Bikron BCD Binary Clock
# Adapted from online sources
# Version 1.9 October 14, 2020
# Unicorn pHat 8 Columns, 4 Rows
#
# New: days and times to display weather info
#  For example, only show weather M-F 08:00 - 17:00
#
# See config.py for options
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
import config as cfg
import logging

LOG_FILE = "/var/log/bikron"
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)

unicorn.set_layout(unicorn.PHAT)
unicorn.brightness(0.5)
unicorn.rotation(0)
width,height=unicorn.get_shape()

# Perform the flip:
if cfg.LSD == 0 :
  unicorn.rotation(180)

# Load the weather with an X until it's updated
# And delay the first update by at least one minute
weather = [52,5]
weather_delay = 3

# Display the weather only on weekdays during working hours
update_days = [1,2,3,4,5] # Mon-Fri
update_hours = ('08:00','18:00')

# Remember user settings for dynamic controls
# to turn weather updates on and off
sav_weather_enable = cfg.weather_enable
sav_temp_enable = cfg.temp_enable
sav_wind_enable = cfg.wind_enable
sav_wday_enable = cfg.wday_enable
sav_month_enable = cfg.month_enable
sav_date_enable = cfg.date_enable

def minutesPerDay(tme):
    hours, minutes = tme.split(':')
    return (hours*60)+minutes

def checkTime(tme, tmeRange):
    return minutesPerDay(tmeRange[0]) <= minutesPerDay(tme) <= minutesPerDay(tmeRange[1])

def checkWeatherUpdate() :
    timenow = time.strftime("%H:%M")
    daynow = int(time.strftime("%w"))
    if daynow not in update_days :
      return False
    return checkTime(timenow, update_hours)

def switchOffWeather() :
      cfg.weather_enable = 0
      cfg.month_enable = 1
      cfg.date_enable = 1

def switchOnWeather() :
      cfg.weather_enable = sav_weather_enable
      cfg.month_enable = sav_month_enable
      cfg.date_enable = sav_date_enable

def GetWeather():
  global weather_delay
  temp = 52
  wind = 5
  if cfg.weather_enable :
    pm = PoolManager()
    try:
      r = pm.request('GET','https://api.weather.com/v2/pws/observations/current?stationId=' + cfg.d['stationID'] + '&format=json&units=e&apiKey=' + cfg.d['api_key'])

      obs = json.loads(r.data.decode('utf-8'))
      temp = obs['observations'][0]['imperial']['temp']
      wind = obs['observations'][0]['imperial']['windSpeed']
    except Exception as ex :
      logging.error(repr(ex))
      weather_delay = 3
      temp = 52
      wind = 5

  mylist = [temp, wind]
  return mylist

def isalarm(ah, am):
  alarmfound = 0
  if os.path.exists(cfg.filepath) :
    with open(cfg.filepath) as fi:
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
  unicorn.off()
#def rainbow

def binclock(bminute):
  # This function will execute for one minute
  global weather, weather_delay, sav_weather_enable

  if weather_delay > 0 :
    cfg.weather_enable = 0 # Temporarily disable weather
    if weather_delay == 1 :
      cfg.weather_enable = sav_weather_enable
      weather = GetWeather()  # Get weather on startup after delay
    weather_delay -= 1

  if checkWeatherUpdate() :
    switchOnWeather()
  else :
    switchOffWeather()

  minint = int(time.strftime("%M"))
  if cfg.refresh.count(minint) and not weather_delay :
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
    if cfg.temp_enable and cfg.weather_enable:
      for x in range(0, 2):
        binary = bin(int(tempd_list[x]))[2:].rjust(4, '0')
        binary_list = list(binary)
        col = x+cfg.temp_col if cfg.LSD else 7-cfg.temp_col-x
        for y in range(0, 4):
          if binary_list[y] == '1':
            unicorn.set_pixel(col,y,cfg.rt,cfg.gt,cfg.bt)
          else:
            unicorn.set_pixel(col,y,cfg.rz,cfg.gz,cfg.bz)

  # Calculate and render WindSpeed
    if cfg.wind_enable and cfg.weather_enable:
      wind = weather[1]
      windd = wind
      if wind > 15 : windd = 15
      wbin = bin(windd) [2:].rjust(4, '0')
      wbin_list = list(wbin)
      col = cfg.wind_col if cfg.LSD else 7-cfg.wind_col
      for y in range(0, 4):
        if wbin_list[y] == '1':
          unicorn.set_pixel(col,y,cfg.rws,cfg.gws,cfg.bws)
        else:
          unicorn.set_pixel(col,y,cfg.rz,cfg.gz,cfg.bz)

  # Render Month
    if cfg.month_enable :
      mobin = bin(int(monthd)) [2:].rjust(4, '0')
      mobin_list = list(mobin)
      col = cfg.month_col if cfg.LSD else 7-cfg.month_col
      for y in range(0, 4):
        if mobin_list[y] == '1':
          unicorn.set_pixel(col,y,cfg.rmo,cfg.gmo,cfg.bmo)
        else:
          unicorn.set_pixel(col,y,cfg.rz,cfg.gz,cfg.bz)


  # Render day of week
    if cfg.wday_enable :
      wdbin = bin(int(wdayd)+1) [2:].rjust(4, '0')
      wdbin_list = list(wdbin)
      col = cfg.wday_col if cfg.LSD else 7-cfg.wday_col
      for y in range(0, 4):
        if wdbin_list[y] == '1':
          unicorn.set_pixel(col,y,cfg.rw,cfg.gw,cfg.bw)
        else:
          unicorn.set_pixel(col,y,cfg.rz,cfg.gz,cfg.bz)


  # Render date
    if cfg.date_enable :
      for x in range(0, 2):
        binary = bin(int(dated_list[x]))[2:].rjust(4, '0')
        binary_list = list(binary)
        col = x+cfg.date_col if cfg.LSD else 7-cfg.date_col-x
        for y in range(0, 4):
          if binary_list[y] == '1':
            unicorn.set_pixel(col,y,cfg.rd,cfg.gd,cfg.bd)
          else:
            unicorn.set_pixel(col,y,cfg.rz,cfg.gz,cfg.bz)

  # Render Seconds
    for x in range(0, 2):
      binary = bin(int(secsd_list[x]))[2:].rjust(4, '0')
      binary_list = list(binary)
      col = (x+cfg.secs_col) if cfg.LSD else (7-cfg.secs_col-x)
      for y in range(0, 4):
        if binary_list[y] == '1':
          unicorn.set_pixel(col,y,cfg.rs,cfg.gs,cfg.bs)
        else:
          unicorn.set_pixel(col,y,cfg.rz,cfg.gz,cfg.bz)

  # Render Minutes
    for x in range(0, 2):
      binary = bin(int(minsd_list[x]))[2:].rjust(4, '0')
      binary_list = list(binary)
      col = (x+cfg.mins_col) if cfg.LSD else (7-cfg.mins_col-x)
      for y in range(0, 4):
        if binary_list[y] == '1':
          unicorn.set_pixel(col,y,cfg.rm,cfg.gm,cfg.bm)
        else:
          unicorn.set_pixel(col,y,cfg.rz,cfg.gz,cfg.bz)


  #Render Hours
    hbin = bin(int(hourd)) [2:].rjust(4, '0')
    hbin_list = list(hbin)
    col = (cfg.hours_col) if cfg.LSD else (7-cfg.hours_col)
    for y in range(0, 4):
      if hbin_list[y] == '1':
        unicorn.set_pixel(col,y,cfg.rh,cfg.gh,cfg.bh)
      else:
        unicorn.set_pixel(col,y,cfg.rz,cfg.gz,cfg.bz)

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

  unicorn.off()

# Main Program

try:
  loop()
except (KeyboardInterrupt):
  destroy()


