#!/usr/bin/python -u

from libbot import *
from math import sqrt
from random import random

init_bot("wolf")
t = 0
while True:
	world_info = get_world()
        me = world_info["me"]
        x = me["pos"]["x"]
        y = me["pos"]["y"]
        hx = me["heading"]["x"]
        hy = me["heading"]["y"]

	bots = world_info["bots"]
	tx = 0
	ty = 0
	found_rabbit = False
	for bot in bots:
		if bot["name"] == "rabbit":
			tx = bot["pos"]["x"]
			ty = bot["pos"]["y"]
			found_rabbit = True

	if found_rabbit:
		dx = tx - x
		dy = ty - y
		mag = sqrt(dx*dx + dy*dy)
		if mag < 10:
			dx = 0
			dy = 0
			dh = (0,0)
		else:
			dx = 2*dx / mag
			dy = 2*dy / mag
			dh = (dx - hx, dy - hy)
	else:
		dx = 0
		dy = 0
		dh = (random() - 0.5 - hx, random() - 0.5 - hy)

	response = dict()
	response["dx"] = {"x" : dx, "y" : dy}
	response["dh"] = {"x" : dh[0], "y" : dh[1]}
	response["att"] = True
	response["str"] = "I see that dang rabbit" if found_rabbit else "where is that dang rabbit??"
	return_update(response)
