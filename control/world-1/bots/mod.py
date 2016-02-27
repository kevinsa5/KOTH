#!/usr/bin/python -u

import sys
sys.path.append('./lib')
from libbot import *

init_bot("mod")
while True:
	world_info = get_world()
	me = world_info["me"]
	bots = world_info["bots"]
	response = dict()
	if me["heading"]["x"] != 1:
		hx = 1 - 0.1*me["heading"]["x"]
	if me["heading"]["y"] != 1:
		hy = 1 - 0.1*me["heading"]["y"]
	response["dx"] = {"x" : -2, "y" : -2}
	response["dh"] = {"x" : hx, "y" : hy}
	response["att"] = False
	response["str"] = ",".join([bot["name"] for bot in bots])
	return_update(response)
