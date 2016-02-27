#!/usr/bin/octave --silent

addpath('./lib');

libbot

init_bot('cow')

while(true)
	world = get_world();
	my_coords = [world.me.pos.x, world.me.pos.y];
	my_heading = [world.me.heading.x, world.me.heading.y];
	found_plant = false;
	plant_coords = [];
	for(i = 1:length(world.bots))
		bot = world.bots(i){1};
		if(strcmp(bot.name, 'plant'))
			found_plant = true;
			plant_coords = [bot.pos.x, bot.pos.y];
			break;
		end
	end
	dx = [0,0];
	dh = [0,0];
	if (found_plant)
		plant_vector = plant_coords - my_coords;
		dh = plant_vector/norm(plant_vector) - my_heading;
		if (norm(plant_vector) > 10)
			dx = plant_vector/norm(plant_vector);
		else
			dx = [0,0];
		end

	else
		dh = rand(1,2) - [0.5,0.5] - my_heading;
	end
	update = struct();
	update.dx = struct('x',dx(1),'y',dx(2));
	update.dh = struct('x',dh(1),'y',dh(2));
	update.att = false;
	update.str = 'moo';
	return_update(update);
end

