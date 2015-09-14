#!/usr/bin/julia

import Base.Pipe, Base.Process
using Redis, JSON

type Point
  x::Float64
  y::Float64
end

type Stats
  attack::Float64
  defense::Float64
  health::Float64
end

type BotState
  name::String
  pos::Point
  heading::Point
  health::Float64
  rechargeTime::Float64
  stats::Stats
  note::String
end

type StateUpdate
  dx::Point
  dheading::Point
  newAttack::Bool
end

type BotProcess
  name::String
  stdin::Pipe
  stdout::Pipe
  process::Process
  state::BotState
end

function parseUpdateDict(d::Dict{AbstractString,Any})
  dx = d["dx"]["x"]
  dy = d["dx"]["y"]
  dhx = d["dh"]["x"]
  dhy = d["dh"]["y"]
  att = d["att"]
  return StateUpdate(Point(dx,dy), Point(dhx, dhy), att)
end

function applyUpdate(state::BotState, delta::StateUpdate)
  if sqrt(delta.dx.x^2 + delta.dx.y^2) > 10
    error("Bot $(state.name) tried to move too fast.")
  end
  state.pos.x += delta.dx.x
  state.pos.y += delta.dx.y

  state.pos.x = state.pos.x < 0 ? 0 : state.pos.x
  state.pos.y = state.pos.y < 0 ? 0 : state.pos.y
  state.pos.x = state.pos.x > 300 ? 300 : state.pos.x
  state.pos.y = state.pos.y > 300 ? 300 : state.pos.y
  
  state.heading.x += delta.dheading.x
  state.heading.y += delta.dheading.y
  if delta.newAttack && state.rechargeTime < 0
    state.rechargeTime = 10
    return "attack"
  end
  return "nothing"
end

conn = RedisConnection()

bot_files = readdir("/usr/lib/cgi-bin/bots")

bots = BotProcess[]

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
	resp = chomp(readline(so))
	stats = Stats(10,10,10)
	state = BotState(resp,Point(rand()*300,rand()*300),Point(0.0,0.0),10,0,stats,"")
	push!(bots, BotProcess(resp, si, so, pr,state))
end

println("Bots setup complete, total number: $(length(bots))")
world = Dict()
bot_states = BotState[]
for bot in bots
	state = BotState(bot.name, Point(rand()*300, rand()*300), Point(rand()-0.5, rand()-0.5), 10, 0, Stats(10,10,10), "Brand New Bot")
	push!(bot_states, state)
end
world["name"] = "First World"
world["bots"] = bot_states

while true
	println("starting new update cycle")
	updates = StateUpdate[]
	for bot in bots
		info = Dict("bots" => world["bots"])
		write(bot.stdin,JSON.json(info) * "\n")
		resp = chomp(readline(bot.stdout))
		println("$(bot.name) said '$resp'")
		update_dict = JSON.parse(resp)
		println("made an update dict")
		update = parseUpdateDict(update_dict)
		println("parsed the dict")
		push!(updates, update)
		println("Done talking with $(bot.name)")
	end
	for (state, update) in zip(bot_states, updates)
		applyUpdate(state, update)
	end
	println("after loops")
	s = JSON.json(world)
	println(s)
	publish(conn, "kev-channel", JSON.json(world))
	println("ending cycle, about to sleep\n")
	sleep(0.1)
end
