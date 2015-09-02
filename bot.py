#!/usr/bin/python -u

import sys
from math import sin, cos

def say(s):
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def listen():
	return sys.stdin.readline().strip()

if __name__ == "__main__":
	greeting = listen()
	if greeting != "KOTH Controller is Ready":
		raise RuntimeError("Controller is talking funny: " + greeting)
	
	say("KOTH Bot is Ready")
	t = 0
	while True:
		info = listen()
		r = 2 + 2*cos(2*t)
		x = (4+r*cos(t))*25
		y = (2+r*sin(t))*50
		say('{"x":%s,"y":%s}' % (x,y))
		t = t + 0.1
