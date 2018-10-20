# -*- coding: utf-8 -*-


from webwhatsapi import WhatsAPIDriver
from git import Repo
import os

# Abstract class to implement WebWhtasapp-Wrapper bots
# Author : Luis Fagundes
# Co-author: Guilherme Lunhani
class Bot(object):

  def __init__(self, **kwargs):
    self.attributes = []
    self.properties = {}
    # Default cache folder must exist!
    p = os.path.abspath(os.path.join(os.getcwd(), '_cache'))
    u = kwargs.get('username')
    c = kwargs.get('client')
    h = kwargs.get('headless')
    self.driver = WhatsAPIDriver(client=c,
                                 username=u,
                                 profile=p,
                                 headless=h)
    

  def setup(self, **kwargs):
    for p in self.attributes:
      m = self.getattribute(p)
      m.setup(kwargs.get(p))

  def run(self, **kwargs):
    while True:
      time.sleep(kwargs.frameTime)
      for message_group in self.driver.get_unread():
        for message in message_group.messages:
          for fn in kwargs.callbacks:
            fn(message_group.chat, message)

  def plugin(self, **kwargs):
    try:
      Repo.clone_from(kwargs.url, kwargs.path)
      sys.path.append("%s" % kwargs.path)
      module = __import__(kwargs.name)
      className = getattr(module, kwargs.name.title())
      instance = className(self.driver)
      self.attributes.push(kwargs.name)
      self.setattr(kwargs.name, instance)
      print str(self.getattribute(kwargs.name))
    except ImportError:
      print "failed import %s" % p

  def getattribute(self, key):
    if key in self.attributes:
      return self.properties[key]
    else:
      raise Exception("no %s attribute found")

  def setattr(self, key, val):
    if key in self.attributes:
      self.properties[key] = val    
    else:
      raise Exception("no %s attribute defined")
