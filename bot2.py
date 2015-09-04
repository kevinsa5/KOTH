#!/usr/bin/python -u

import sys, json
from math import sin, cos, sqrt

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
	say("wolf")
	x = 0
	y = 0
	while True:
		world_info = json.loads(listen())
		bots = world_info["bots"]
		tx = 0
		ty = 0
		for bot in bots:
			if bot["name"] == "rabbit":
				tx = bot["x"]
				ty = bot["y"]
				break
		dx = tx - x
		dy = ty - y
		mag = sqrt(dx*dx + dy*dy)
		if mag != 0:
			dx = 2*dx / mag
			dy = 2*dy / mag
			x = x + dx
			y = y + dy
		say('{"x":%s,"y":%s,"name":"wolf"}' % (x,y))
