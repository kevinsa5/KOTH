#!/usr/bin/python -u

from libbot import *
from math import sqrt
from random import random

init_bot("mouse")
target = [100,200]
t = 0
chirality = 1
while True:
	world_info = get_world()
	me = world_info["me"]
	x = me["pos"]["x"]
	y = me["pos"]["y"]
	hx = me["heading"]["x"]
	hy = me["heading"]["y"]
	catx = 0
	caty = 0
	cat_found = False
	for bot in world_info["bots"]:
		if bot["name"] == "cat":
			catx = bot["pos"]["x"]
			caty = bot["pos"]["y"]
			cat_found = True
			break
	
	if t % 50 == 0:
		chirality = -1 * chirality
	if cat_found:
		cat_vector = [x - catx, y - caty]
		mag = sqrt(sum(i*i for i in cat_vector))
		if mag != 0:
			cat_vector = [i / mag for i in cat_vector]
		# run perpendicular to the wolf's approach:
		run = [chirality * cat_vector[1], -1 * chirality * cat_vector[0]]
	
		# but also away from the cat a little bit:
		run[0] = run[0] + cat_vector[0]
		run[1] = run[1] + cat_vector[1]
		
		run[0] = 3*run[0]
		run[1] = 3*run[1]
		
		# always watch that pesky cat:
		dh = (-hx - cat_vector[0], -hy - cat_vector[1])
	else:
		run = (0,0)
		dh = (random()-0.5 - hx, random() - 0.5 - hy)
	update = dict()
	update["dx"] = {"x" : run[0], "y" : run[1]}
	update["dh"] = {"x" : dh[0]     , "y" : dh[1]}
	update["att"] = False
	update["str"] = "Eek!  I see a cat!" if cat_found else "Hmm where is a cheese."
	return_update(update)
	t = t + 1
