#!/usr/bin/python

from time import strftime, sleep
import cgi
"""
_count = 0

def exitfunc():
	global _count
	open("~/poop.txt","w").write("%d" % _count)

import atexit
atexit.register(exitfunc)
"""
print "Content-Type: text/event-stream; charset=utf-8"
print

while True:
	print "event: hooray"
	print "data: %s" % strftime("%Y-%m-%d %H:%M:%S")
	sleep(1)
