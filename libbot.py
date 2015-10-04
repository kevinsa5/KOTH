import sys, json

def say(s):
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def listen():
	return sys.stdin.readline().strip()

def init_bot(name):
	greeting = listen()
        if greeting != "KOTH Controller is Ready":
                raise RuntimeError("Controller is talking funny: " + greeting)

        say("KOTH Bot is Ready")
        query = listen()
        if query != "What is your name?":
                raise RuntimeError("It didn't ask me my name! '{}'".format(query))
        say(name)

def get_world():
	return json.loads(listen())

def return_update(d):
	say(json.dumps(d))
