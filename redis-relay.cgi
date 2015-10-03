#!/usr/bin/python
import sys
import datetime
import time
import redis
import cgi

args = cgi.FieldStorage()
channel = args["world"].value

config = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

r = redis.StrictRedis(**config)
pubsub = r.pubsub()
pubsub.subscribe(channel)

sys.stdout.write('Content-type: text/event-stream \n\n')

while True:
	for item in pubsub.listen():
		sys.stdout.write('data: %s \n\n' % item['data'])
		sys.stdout.flush()
