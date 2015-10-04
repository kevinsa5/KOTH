#!/usr/bin/octave --silent

% use input("","s") as readline
% see http://sourceforge.net/projects/iso2mesh/files/jsonlab/

function s = listen()
	s = input("","s")
end

function say(s)
	printf(s);
	printf('\n');
end

