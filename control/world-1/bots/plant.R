#!/usr/bin/Rscript --quiet

source("./lib/libbot.R");

init_bot("plant");

while(TRUE){
	world = get_world();
	
	response = list();
	# the json library requires scalars to be unboxed, or else it will treat them like
	# vectors.  maybe make libbot.R go through and do this for the user.
	response$dx = list("x" = unbox(0), "y" = unbox(0));
	response$dh = list("x" = unbox(0), "y" = unbox(0));
	response$att = unbox(FALSE);
	response$str = unbox("hallo");
	return_update(response);	
}
