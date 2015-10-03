#!/usr/bin/python -u

from libbot import *
from math import sqrt
from random import random

init_bot("cat")
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
	found_mouse = False
	for bot in bots:
		if bot["name"] == "mouse":
			tx = bot["pos"]["x"]
			ty = bot["pos"]["y"]
			found_mouse = True

	if found_mouse:
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
	response["att"] = False
	response["str"] = "gonna get that mouse" if found_mouse else "nasty little mouse, where is it?"
	return_update(response)
