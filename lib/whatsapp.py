# Import os and check for SELENIUM* environment variables
import os
import sys

# Initialize Driver (See for selenium url)
try:
  os.environ["SELENIUM"]  
except KeyError:
  print "Please set the environment variable SELENIUM to Selenium URL"
  sys.exit(1)

# Now imports
import sys
import time
import os
import argparse
import json
sys.path.append(os.getcwd())
import bot

# Arg parser
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username')
parser.add_argument('-c', '--config')
parser.add_argument('-C', '--client')
parser.add_argument('-p', '--profile')
parser.add_argument('-H', '--headless', action='store_true')
args = parser.parse_args()

# Implement a abstract bot,
# with setup and run functions,
# Like a Java Processing Art Framework
class WebWhatsappWrapperBot(bot.Bot):

  def __init__(self, **kwargs):
    super(WebWhatsappWrapperBot, self).__init__(**kwargs)
    
    # Open and loads configuration for each
    # plugin
    self.config = {}
    with open(kwargs.config) as json_data:
      d = json.load(json_data)
      for key,val in d.iteritems():
        p = os.path.abspath(os.getcwd(), key)
        self.plugin(name=key,
                    url=val.url,
                    path=p)
        self.config[key] = val.config   

  # A simple implementation of setup
  # loaded form configuration readed by a json file
  def setup(self):  
    super.setup(self.config)
    for key, val in self.config.iteritems():
      print "%s: %s" % (key, val)

  # A simple implementation of run with 0.1 seconds
  # between a call and another call, with
  # implementation of handle methods of each plugin
  def run(self):
    handles = [] 
    for key, val in self.config.iteritems():
      handle = self.__getattribute__(key).handle
      handles.append(handle)
    super.run(frameTime=0.1, callbacks=handles)
      
# Run bot
www = WebWhatsappWrapperBot(client=args.client,
                            username=args.username,
                            config=args.config,
                            headless=args.headless)
www.setup()
www.run()
