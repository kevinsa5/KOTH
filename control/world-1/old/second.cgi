#!/usr/bin/python
import sys
import datetime
import time

sys.stdout.write('Content-type: text/event-stream \n\n')

while True:
	now = datetime.datetime.now()
	sys.stdout.write('data: %s \n\n' % now)
	sys.stdout.flush()
	time.sleep(1)

#sys.stdout.write('retry: 1000\r\n\r\n')
