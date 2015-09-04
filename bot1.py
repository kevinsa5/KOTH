#!/usr/bin/python -u

import sys, json
from math import sin, cos, sqrt
from random import random

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
        query = listen()
        if query != "What is your name?":
                raise RuntimeError("It didn't ask me my name! '{}'".format(query))
        say("rabbit")

	pos = [100,100]
	target = [100,200]
	t = 0
	while True:
		world_info = json.loads(listen())
		if t % 50 == 0:
			target = [random()*300, random()*300]
		heading = [target[0] - pos[0], target[1] - pos[1]]
		mag = sqrt(sum(i*i for i in heading))
		if mag != 0 and mag > 5:
			heading = [4*i/mag for i in heading]
			pos = [pos[0] + heading[0], pos[1] + heading[1]]
		say('{"x":%s,"y":%s,"name":"rabbit"}' % (pos[0],pos[1]))
		t = t + 1
