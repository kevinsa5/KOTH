#!/usr/bin/Rscript --quiet

source("./bots/libbot.R");

init_bot("plant");

while(TRUE){
	world = get_world();
	
	response = list();
	response$dx = list("x" = unbox(0), "y" = unbox(0));
	response$dh = list("x" = unbox(0), "y" = unbox(0));
	response$att = unbox(FALSE);
	response$str = unbox("hallo");
	return_update(response);	
}
