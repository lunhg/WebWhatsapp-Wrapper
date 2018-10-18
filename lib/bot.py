# -*- coding: utf-8 -*-

import time, os, json
from elasticsearch import Elasticsearch
from webwhatsapi import WhatsAPIDriver

# Author : Luis Fagundes
# Co-author: Guilherme Lunhani
class Bot:

  def __init__(self, username, profile, config, headless=True):
    # Initialize Driver
    self.driver = WhatsAPIDriver(username=username, profile=profile, headless=headless)

    # Initialize ElasticSearch
    self.es = Elasticsearch(config)
    self.logdir = os.path.join(os.path.dirname(__file__), '..', 'log')
    self.datadir = os.path.join(os.path.dirname(__file__), '..', 'data')

    # Log
    __log__ = "%s_log.json" % username
    log = os.path.join(logdir, __log__)
    self.logfh = open(log, "a")
    if (self.logfh.tell() == 0):
      self.logfh.write('[]')
      self.logfh.flush()

  def run(self):
    while True:
      time.sleep(0.1)
      for message_group in self.driver.get_unread():
        for message in message_group.messages:
          self.handle(message_group.chat, message)

  def handle(self, chat, message):
    self.log(chat, message)
    result = self.es.search(index='memes', body={
      'query': {
        'match': {
          'tag': message.content
        }
      }
    })
    hits = result['hits']['hits']
    if len(hits) == 0:
      chat.send_message('Não achei nenhum meme com essas palavras')
      return
    hits = hits[:3]
    hits.reverse()
    for meme in hits:
      self.driver.send_media(meme['_source']['path'], chat.id, '')


  def log(self, chat, message):
    msg = {
      'uid': chat.id,
      'msg': message.content,
      'tim': int(time.time()),
    }
    pos = self.logfh.tell()
    self.logfh.seek(pos-1)
    self.logfh.truncate()
    if (pos > 2):
      self.logfh.write(', ')
      self.logfh.write(json.dumps(msg))
      self.logfh.write(']')
      self.logfh.flush()
