#!/usr/bin/python

import web
import serial

urls = ('/(.*)', 'hello')
app = web.application(urls, globals())
Serial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

###############################################################################
###############################################################################
class hello:
  def GET(self, name):
    if not name:
      name = 'World'
    return 'Hello, ' + name + '!'

###############################################################################
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
  print 'Red =',   Red
  print 'Blue =',  Blue
  print 'Green =', Green
  print 'Alpha =', Alpha
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
###############################################################################
if __name__ == "__main__":
  app.run()
