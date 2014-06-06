#!/usr/bin/python

import web
import serial
import RPi.GPIO as gpio

urls = ('/(.*)', 'hello')
app = web.application(urls, globals())
try:
 Serial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
except:
  print 'Serial Connection could not be established'
  exit()
try:
  gpio.setmode(gpio.BOARD)
  gpio.setup(12, gpio.OUT)
  gpio.output(12,1)
except:
  print 'GPIO could not setup properly'
  exit()

###############################################################################
###############################################################################
class hello:
  def POST(*args,**kwargs):
    Data  = web.input()
    if 'Type' in Data:
      Type = Data['Type']
      if 'jColor' in Type:
        return GetColors(Data,'j')
      elif 'fColor' in Type:
        return GetColors(Data,'f')
      elif 'Mode' in Type:
        return GetModeData(Data)
      elif 'LaserToggle' in Type:
        return GetLaserToggleData(Data)
      else:
        return 'ERROR'

###############################################################################
###############################################################################
def GetColors(Data,FadeOrJump):
  Red   = GetFloat('Red',   Data)
  Blue  = GetFloat('Blue',  Data)
  Green = GetFloat('Green', Data)
  Alpha = GetFloat('Alpha', Data)
  Serial.write("<"+FadeOrJump+"Color,")
  Serial.write(str(Alpha)+ ',')
  Serial.write(str(Red) + ',')
  Serial.write(str(Green) + ',' + str(Blue) + ">")
  return Red, Blue, Green, Alpha

###############################################################################
def GetFloat(Float, Data):
  if Float in Data:
    try:
      return float(Data[Float])
    except:
      return None

###############################################################################
def GetBool(Value, Data):
  if Value in Data:
    return Data[Value] == 'true'
  else:
    return False

###############################################################################
def GetModeData(Data):
  if 'Mode' in Data:
    Mode = Data['Mode'].replace(' ','')
  else:
    Mode = "RollingColor"
  Frequency = GetFloat('Frequency', Data)
  Serial.write("<Mode,")
  Serial.write(str(Mode)+","+str(Frequency) + ",Null,Null>")

###############################################################################
def GetLaserToggleData(Data):
  if 'Value' in Data:
    if 'true' in Data['Value']:
      gpio.output(12,0)
      return
  gpio.output(12,1)

###############################################################################
###############################################################################
if __name__ == "__main__":
  web.config.debug = False
  try:
    app.run()
  except:
    print 'webpy didnt work'
    exit()
