#!/usr/bin/python -u

from libbot import *
from math import sqrt

init_bot("cat")
x = 0
y = 0
while True:
	world_info = json.loads(listen())
	bots = world_info["bots"]
	tx = 0
	ty = 0
	for bot in bots:
		if bot["name"] == "cat":
			x = bot["pos"]["x"]
			y = bot["pos"]["y"]
		elif bot["name"] == "mouse":
			tx = bot["pos"]["x"]
			ty = bot["pos"]["y"]
	dx = tx - x
	dy = ty - y
	mag = sqrt(dx*dx + dy*dy)
	if mag != 0:
		dx = 2*dx / mag
		dy = 2*dy / mag
	say('{"dx":{"x":%s,"y":%s}, "dh":{"x":0.0,"y":0.0}, "att":false}' % (dx,dy))
	
