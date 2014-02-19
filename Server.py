#!/usr/bin/python

import web

urls = ('/(.*)', 'hello')
app = web.application(urls, globals())

class hello:
  def GET(self, name):
    if not name:
      name = 'World'
    return 'Hello, ' + name + '!'
  def POST(*args,**kwargs):
    data = web.data()
    stuff = web.input()
    print 'data =', data
    print 'stuff =',stuff

if __name__ == "__main__":
  app.run()
