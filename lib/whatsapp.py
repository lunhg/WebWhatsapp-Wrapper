# Imports
import os
import sys
import argparse

# Local imports
sys.path.append(os.getcwd())
import bot


# Arg parser
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username')
parser.add_argument('-p', '--profile')
parser.add_argument('-H', '--elastic-search-host')
parser.add_argument('-P', '--elastic-search-port')
args = parser.parse_args()

# Lets program
username = args.username
profile = ''
if not args.profile:
  profile = os.path.join(os.path.dirname(__file__), '..', '_cache') 
else:
  profile = args.profile

# TODO add replicas
elSearch = [
  {
    'host': args.elastic_search_host or 'localhost',
    'port': args.elastic_search_port or '9200'
  }
]
b = bot.Bot(username, profile, elSearch)
b.run()
