#!/usr/bin/python
# -*- coding: utf-8 -*- 
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#--------------------------------------
from doconfig import *
import smbus
import time
import socket
from datetime import datetime
from subprocess import call
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# Le GPIO 23 est initialisé en entrée. Il est en pull-up pour éviter les faux signaux
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define some device parameters
I2C_ADDR  = 0x3f # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

red = 17
green = 18
blue = 27
# GPIO setup.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

# Set up colors using PWM so we can control individual brightness.
RED = GPIO.PWM(red, 100)
GREEN = GPIO.PWM(green, 100)
BLUE = GPIO.PWM(blue, 100)
RED.start(0)
GREEN.start(0)
BLUE.start(0)

cList = conf_open()
oBjs = get_conf(cList)
for oo in oBjs:
    doThisShit(oo)


def lcd_init():
    # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
    # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
      lcd_byte(ord(message[i]),LCD_CHR)

# Set a color by giving R, G, and B values of 0-255.
def setColor(rgb = []):
    # Convert 0-255 range to 0-100.
    rgb = [(x / 255.0) * 100 for x in rgb]
    RED.ChangeDutyCycle(rgb[0])
    GREEN.ChangeDutyCycle(rgb[1])
    BLUE.ChangeDutyCycle(rgb[2])

def set_medoc_time():
    date = datetime.now()
    hour = date.hour
    minute = date.minute + 10
    #heuredeprise = medoc.hours[medoc.n_hours].split(':')[0]
    #minutedeprise = medoc.hours[medoc.n_hours].split(':')[1]
    second = 0
    year = date.year
    month = date.month
    day = date.day
    medoc_time = datetime(year, month, day, hour, minute, second, 0)
    print "Set medoc_time:"
    print "date: " + str(year) + "-" + str(month) + "-" + str(day)
    print "hour: " + str(hour) + "-" + str(minute) + "-" + str(second)
    return medoc_time

def switch_led_onoff(stateled):
    if stateled:
        setColor([0, 0, 0])
    else:
        setColor([0, 255, 0])

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def main():
    # Main program block

  # Initialize display
  lcd_init()
  # Init GPIO detection
  GPIO.add_event_detect(23, GPIO.FALLING)
  GPIO.add_event_detect(24, GPIO.FALLING)
  # Init
  medoc_ok = 0
  stateled = 1

  # SHOW IP ADDRESS
  show_ip = get_ip_address() 
  print "IP address: " + show_ip
  lcd_string( show_ip, LCD_LINE_1 )
  while True:
      if GPIO.event_detected(23):
          break

  # Init
  medoc = Medoc()
  medoc.setMedoc(oBjs[-1])
  message = "Coucou Papi"
  heuredeprise = medoc.hours[0].split(':')[0]
  minutedeprise = medoc.hours[0].split(':')[1]

  date = datetime.now()
  year = '{:0>2}'.format(str(date.year))
  month = '{:0>2}'.format(str(date.month))
  day = '{:0>2}'.format(str(date.day))

# DEBUG
  print "Medoc: \n" + heuredeprise + ":" + minutedeprise
  print "date: " + str(year) + "-" + str(month) + "-" + str(day)
  #print "hour: " + str(hour) + "-" + str(minute) + "-" + str(second)

  medoc_time = datetime(int(year), int(month), int(day), int(heuredeprise), int(minutedeprise), 0, 0)
  #medoc_time = datetime(2017, 10, 1, int(heuredeprise), int(minutedeprise), 0, 0)

  while True:

      # Get date object
      date = datetime.now()

      hour = '{:0>2}'.format(str(date.hour))
      minute = '{:0>2}'.format(str(date.minute))
      second = '{:0>2}'.format(str(date.second))

      # Send some test
      lcd_string( hour + ':' + minute + ':' + second, LCD_LINE_1 )
      if GPIO.event_detected(23) and not medoc_ok:
          lcd_string( "Traitement pris", LCD_LINE_2 )
          medoc_time = set_medoc_time()
          medoc_ok = 1
          setColor([255, 255, 255])
          time.sleep(2)
      if GPIO.event_detected(24):
        if stateled:
            setColor([255, 0, 255])
            stateled = 0
        else:
            setColor([255, 255, 255])
            stateled = 1
            time.sleep(1)
      elif date > medoc_time and not medoc_ok:
          lcd_string( medoc.name, LCD_LINE_2 )
          setColor([65, 255, 255])
      else:
          medoc_ok = 0
          lcd_string( message, LCD_LINE_2 )

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        GPIO.cleanup()           # reinitialisation GPIO lors d'une sortie normale

