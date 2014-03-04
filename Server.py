#!/usr/bin/python

import web

urls = ('/(.*)', 'hello')
app = web.application(urls, globals())

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
      if 'Color' in Type:
        return GetColors(Data)
      elif 'Slosh' in Type:
        return GetSloshData(Data)
      else:
        return 'ERROR'

###############################################################################
###############################################################################
def GetColors(Data):
  Red   = GetFloatValue('Red',   Data)
  Blue  = GetFloatValue('Blue',  Data)
  Green = GetFloatValue('Green', Data)
  Alpha = GetFloatValue('Alpha', Data)
  print 'Red =',   Red
  print 'Blue =',  Blue
  print 'Green =', Green
  print 'Alpha =', Alpha
  return Red, Blue, Green, Alpha

###############################################################################
def GetFloatValue(Float, Data):
  if Float in Data:
    try:
      return float(Data[Float])
    except:
      return None

###############################################################################
def GetBool(Value, Data):
  if Value in Data:
    return bool(Data[Value])
  else:
    return False

###############################################################################
def GetSloshData(Data):
  Horizontal = GetBool('Horizontal', Data)
  Vertical   = GetBool('Vertical'  , Data)
  Freq       = GetFloatValue('Frequency', Data)


if __name__ == "__main__":
  app.run()
