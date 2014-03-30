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
      elif 'Slosh' in Type:
        return GetSloshData(Data)
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
def GetSloshData(Data):
  Freq       = GetFloat('Frequency', Data)
  Serial.write("<Slosh,")
  Serial.write("Null,Null,"+str(Freq) + ",Null>")


if __name__ == "__main__":
  app.run()
