% the first line in this file can't be a function definition, and we need this anyway:
addpath("/usr/lib/octave/jsonlab");

% see http://sourceforge.net/projects/iso2mesh/files/jsonlab/

function s = listen()
        s = input("","s");
end

function say(s)
        printf(s);
        printf('\n');
end

function init_bot(name)
        greeting = listen();
        if (~ strcmp(greeting,'KOTH Controller is Ready'))
                error(strcat('Controller is talking funny: ', greeting));
        end
        say('KOTH Bot is Ready');
        query = listen();
        if (~ strcmp(query, 'What is your name?'))
                error(strcat('It didn''t ask me my name! ', query)); 
        end
        say(name);
end

function return_update(d)
        say(savejson("",d,'Compact',true));
end

function w = get_world()
        w = loadjson(listen());
end


