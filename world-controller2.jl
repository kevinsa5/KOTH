#!/usr/bin/julia

import Base.Pipe, Base.Process
using Redis, JSON

type Bot
  name::String
  stdin::Pipe
  stdout::Pipe
  process::Process
end

conn = RedisConnection()

bot_files = readdir("/usr/lib/cgi-bin/bots")

bots = Bot[]

for (i, bot_file) in enumerate(bot_files)
	(so, si, pr) = readandwrite(`/usr/lib/cgi-bin/bots/$bot_file`)
	write(si, "KOTH Controller is Ready\n")
	resp = readline(so)
	if resp == "KOTH Bot is Ready\n"
		println("KOTH Bot #$i responded correctly.")
	else
		error("KOTH Bot #$i is talking funny: '$resp'. Skipped. ")
		continue
	end
	write(si, "What is your name?\n")
	resp = readline(so)
	push!(bots, Bot(resp, si, so, pr))
end

println("Bots setup complete, total number: $(length(bots))")
old_world = Dict()
bot_states = Dict[]
for bot in bots
	push!(bot_states, Dict("x"=>rand()*300, "y"=>rand()*300, "name"=>bot.name))
end
old_world["name"] = "First World"
old_world["bots"] = bot_states

while true
	println("starting new update cycle")
	new_world = Dict()
	new_world["name"] = "First World"
	bot_states = Dict[]
	for bot in bots
		write(bot.stdin,JSON.json(old_world) * "\n")
		resp = chomp(readline(bot.stdout))
		println("$(bot.name) said '$resp'")
		bot_state = JSON.parse(resp)
		push!(bot_states, bot_state)
	end
	println("after loop")
	new_world["bots"] = bot_states
	publish(conn, "kev-channel", JSON.json(new_world))
	old_world = new_world
	println("ending cycle, about to sleep\n")
	sleep(0.1)
end
