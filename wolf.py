#!/usr/bin/python -u

from libbot import *
from math import sqrt

init_bot("wolf")
x = 0
y = 0
while True:
	world_info = json.loads(listen())
        me = world_info["me"]
        x = me["pos"]["x"]
        y = me["pos"]["y"]
        hx = me["heading"]["x"]
        hy = me["heading"]["y"]

	bots = world_info["bots"]
	tx = 0
	ty = 0
	for bot in bots:
		if bot["name"] == "rabbit":
			tx = bot["pos"]["x"]
			ty = bot["pos"]["y"]
	dx = tx - x
	dy = ty - y
	mag = sqrt(dx*dx + dy*dy)
	if mag != 0:
		dx = 2*dx / mag
		dy = 2*dy / mag
	response = dict()
	response["dx"] = {"x" : dx, "y" : dy}
	response["dh"] = {"x" : dx-hx, "y" : dy - hy}
	response["att"] = False
	return_update(response)
