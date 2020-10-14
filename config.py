#!/usr/bin/env python

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

# Least Significant Digit at the top?: true or false
LSD = 1

#----Colors - Default Rainbow
rt, gt, bt = COLORS['maroon'] #Temperature
rws, gws, bws = COLORS['olive'] #Wind
rh, gh, bh = COLORS['green'] #Hours
rm, gm, bm = COLORS['teal'] #Minutes
rs, gs, bs = COLORS['purple'] #Seconds
rz, gz, bz = COLORS['black'] #Background 'off' color

#Options
rmo, gmo, bmo = COLORS['maroon'] #Month
rw, gw, bw = COLORS['maroon'] #Weekday
rd, gd, bd = COLORS['olive'] #Date

#----Column Assignments
# Columns are numbered 76543210 left to right
#right Temperature Column (2 columns)
temp_col = 6
# WindSpeed Column (1 column)
wind_col = 5
#Hours Column (1 column)
hours_col = 4
#right Minutes Column (2 columns)
mins_col = 2
#right Seconds Column (2 columns)
secs_col = 0
#Options
#Weekday (1 column)
wday_col = 7
#Month (1 column)
month_col = 7
#right Date Column (2 columns)
date_col = 5

#----Enable options
wday_enable = 0
#Month (1 column)
month_enable = 0
#right Date Column (2 columns)
date_enable = 0
#right Temperature Column (2 columns)
temp_enable = 1
# WindSpeed Column (1 column)
wind_enable = 1
# GetWeather Control
weather_enable = 1
refresh = [8, 18, 28, 38, 48, 58] # Weather on the 8's
d = {'api_key': 'yourapikey',
     'stationID': 'yourstationid'}

filepath = '/home/pi/Bikron/alarms.txt'


