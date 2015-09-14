#!/usr/bin/python -u

from libbot import *
from math import sqrt

init_bot("mouse")
target = [100,200]
t = 0
chirality = 1
while True:
	world_info = json.loads(listen())
	me = world_info["me"]
	x = me["pos"]["x"]
	y = me["pos"]["y"]
	hx = me["heading"]["x"]
	hy = me["heading"]["y"]
	catx = 0
	caty = 0
	for bot in world_info["bots"]:
		if bot["name"] == "cat":
			catx = bot["pos"]["x"]
			caty = bot["pos"]["y"]
			break
	
	if t % 50 == 0:
		chirality = -1 * chirality

	cat_vector = [x - catx, y - caty]
	mag = sqrt(sum(i*i for i in cat_vector))
	if mag != 0:
		cat_vector = [i / mag for i in cat_vector]
	# run perpendicular to the wolf's approach:
	heading = [chirality * cat_vector[1], -1 * chirality * cat_vector[0]]

	# but also away from the cat a little bit:
	heading[0] = heading[0] + cat_vector[0]
	heading[1] = heading[1] + cat_vector[1]
	
	heading[0] = 3*heading[0]
	heading[1] = 3*heading[1]

	dh = (heading[0] - hx, heading[1] - hy)
	update = dict()
	update["dx"] = {"x" : heading[0], "y" : heading[1]}
	update["dh"] = {"x" : dh[0]     , "y" : dh[1]}
	update["att"] = False
	return_update(update)
	t = t + 1
