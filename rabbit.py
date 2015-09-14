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

	target = [100,200]
	t = 0
	while True:
		world_info = json.loads(listen())
		me = world_info["me"]
		pos = [me["pos"]["x"], me["pos"]["y"]]
		oldheading = [me["heading"]["x"], me["heading"]["y"]]
		if t % 50 == 0:
			target = [random()*300, random()*300]
		heading = [target[0] - pos[0], target[1] - pos[1]]
		mag = sqrt(sum(i*i for i in heading))
		if mag != 0 and mag > 5:
			heading = [4*i/mag for i in heading]
		dh = [heading[0] - oldheading[0], heading[1] - oldheading[1]]
		say('{"dx":{"x":%s,"y":%s}, "dh":{"x":%s,"y":%s}, "att":false}' % (heading[0],heading[1], dh[0], dh[1]))
		t = t + 1
