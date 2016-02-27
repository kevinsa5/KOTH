suppressMessages(library(jsonlite))

say = function(s){
	cat(paste0(s,"\n"));
}
stdin_file = file("stdin")
listen = function(){
	return(readLines(stdin_file,1));
}

init_bot = function(name){
	greeting = listen()
	if(greeting != "KOTH Controller is Ready"){
		stop(paste("Controller is talking funny:", greeting));
	}
	say("KOTH Bot is Ready");
	query = listen();
	if(query != "What is your name?"){
		stop(paste0("It didn't ask me my name! '", greeting, "'"));
	}
	say(name);
}

get_world = function(){
	return(fromJSON(listen()));
}

return_update = function(f){
	say(toJSON(f));
}
