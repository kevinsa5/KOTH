#!/usr/bin/python -u

import sys
sys.path.append('./lib')
from libbot import *
from math import sin, cos, sqrt
from random import random

if __name__ == "__main__":
	init_bot("rabbit")

	target = [100,200]
	t = 0
	while True:
		world_info = get_world()
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
		update = dict()
		update["dx"] = {"x" : heading[0], "y" : heading[1]}
		update["dh"] = {"x" : dh[0], "y" : dh[1]}
		update["att"] = False
		update["str"] = "so... tired..." if mag < 1 else "oh god oh god"
		return_update(update)
		t = t + 1
