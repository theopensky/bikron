#!/usr/bin/env python
# Bikron BCD Binary Clock
# Adapted from online sources
# Version 1.4 September 24, 2020
# Unicorn pHat 8 Columns, 4 Rows
# 
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

import unicornhat as unicorn
import time
import colorsys
import math
import os.path

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
#Date Column 0-7
date_col = 5
rd, gd, bd = COLORS['purple']
#Hours Column 0-7
hours_col = 4
rh, gh, bh = COLORS['maroon']
#right Minutes Column 0-7
mins_col = 2
rm, gm, bm = COLORS['teal']
#right Seconds Column 0-7
secs_col = 0
rs, gs, bs = COLORS['green']
#Weekday
wday_col = 7
rw, gw, bw = COLORS['olive']
#background OFF color
rz, gz, bz = COLORS['black']

def isalarm(ah, am):
  alarmfound = 0
  filepath = '/home/pi/alarms.txt'
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
  minint = int(time.strftime("%M"))
  while (bminute == minint):
    minint = int(time.strftime("%M"))
    secsd = time.strftime("%S") [::-1]
    minsd = time.strftime("%M") [::-1]
    hourd = time.strftime("%I")
    dated = time.strftime("%d") [::-1]
    wdayd = time.strftime("%w")
    secsd_list = list(secsd)
    minsd_list = list(minsd)
    dated_list = list(dated)

  # Render day of week
    wdbin = bin(int(wdayd)+1) [2:].rjust(4, '0')
    wdbin_list = list(wdbin)
    for y in range(0, 4):
      if wdbin_list[y] == '1':
        unicorn.set_pixel(wday_col,y,rw,gw,bw)
      else:
        unicorn.set_pixel(wday_col,y,rz,gz,bz)


  # Render date
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

# Main Program
# Check for an alarm in the alarms.txt file
# If HR:MM matches, play the rainbow for one minute
# otherwise just run the clock for one minute
# repeat
# To set or delete alarms, simply modify alarms.txt

while 1:
  minint = int(time.strftime("%M"))
  hrsint = int(time.strftime("%H"))
  if isalarm(hrsint, minint):
     rainbow(minint)
  minint = int(time.strftime("%M"))
  binclock(minint)

unicorn.clear
