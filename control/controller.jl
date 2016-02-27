#!/usr/bin/julia

import Base.Pipe, Base.Process
using Redis, JSON

if length(ARGS) > 0
	WORLD_NAME = ARGS[1]
else
	WORLD_NAME = "Default-World"
end
DEBUG = false

println("Creating world '$WORLD_NAME'...")

function debug_println(s::ASCIIString)
  if DEBUG
    println(s)
  end
end

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
  str::String
end

type BotProcess
  name::String
  stdin::Pipe
  stdout::Pipe
  process::Process
  state::BotState
  active::Bool
end


# the bots might not return all fields, so we have to wrap the parsing
function parseUpdateDict(d::Dict{AbstractString,Any})
  dx = get(d,"dx",None)
  if dx == None
    dxx = 0
    dxy = 0
  else
    dxx = get(dx, "x", 0)
    dxy = get(dx, "y", 0)
  end
  dh = get(d,"dh",None)
  if dh == None
    dhx = 0
    dhy = 0
  else
    dhx = get(dh,"x",0)
    dhy = get(dh,"y",0)
  end
  att = get(d, "att", false)
  str = get(d, "str", "")
  return StateUpdate(Point(dxx,dxy), Point(dhx, dhy), att, str)
end

function applyUpdate(state::BotState, delta::StateUpdate, visible_bots::Array{BotState})
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
  if state.rechargeTime > 0
    state.rechargeTime -= 0.25
  end
  if delta.newAttack && state.rechargeTime <= 0
    for bot in visible_bots
      dist = sqrt((bot.pos.x - state.pos.x)^2 + (bot.pos.y - state.pos.y)^2)
      if dist < 25
        bot.health -= 1
      end
    end
    state.rechargeTime = 10
  end
  if delta.str != ""
    state.note = delta.str
  end
end

function getVisibleBots(bot_list::Array, bot::BotState)
  x = bot.pos.x
  y = bot.pos.y
  hx = bot.heading.x
  hy = bot.heading.y
  looking_direction = atan2(hy,hx)
  visible_bots = BotState[]
  for b in bot_list
    if b == bot
      continue
    end
    dx = b.pos.x - x
    dy = b.pos.y - y
    direction = atan2(dy,dx)
    visible = pi - abs((abs(direction - looking_direction) % (2*pi)) - pi) < pi/4
    if visible
      debug_println("found a visible bot")
      push!(visible_bots, b)
    end
  end
  return visible_bots
end

conn = RedisConnection()

dir = dirname(Base.source_path())

bot_files = readdir(dir * "/" * WORLD_NAME * "/bots")

bots = BotProcess[]

for bot_file in bot_files
	# skip filenames beginning with "lib"
	if ismatch(r"^lib", bot_file)
		continue
	end
	println("Using bot: $bot_file");
	(so, si, pr) = readandwrite(`./$WORLD_NAME/bots/$bot_file`)
	write(si, "KOTH Controller is Ready\n")
	resp = readline(so)
	if resp == "KOTH Bot is Ready\n"
		debug_println("KOTH Bot '$bot_file' responded correctly.")
	else
		error("KOTH Bot '$bot_file' is talking funny: '$resp'. Skipped. ")
		continue
	end
	write(si, "What is your name?\n")
	resp = chomp(readline(so))
	stats = Stats(10,10,10)
	state = BotState(resp, Point(rand()*300, rand()*300), Point(rand()-0.5, rand()-0.5), 10, 0, Stats(10,10,10), "Brand New Bot")
	push!(bots, BotProcess(resp, si, so, pr, state, true))
end

println("Bots setup complete, total number: $(length(bots))")

while true
	debug_println("starting new update cycle")
	updates = StateUpdate[]
	active_bots = filter(b -> b.active, bots)
	bot_states = [b.state for b in active_bots]
	for bot in active_bots
		state = bot.state
		info = Dict{ASCIIString,Any}()
		info["bots"] = getVisibleBots(bot_states, state)
		info["me"] = state
		debug_println(JSON.json(info));
		write(bot.stdin,JSON.json(info) * "\n")
		resp = chomp(readline(bot.stdout))
		debug_println("$(bot.name) said '$resp'")
		update_dict = JSON.parse(resp)
		update = parseUpdateDict(update_dict)
		push!(updates, update)
		debug_println("Done talking with $(bot.name)")
	end
	for (state, update) in zip(bot_states, updates)
		applyUpdate(state, update, getVisibleBots(bot_states, state))
	end
	
	killed_bots = filter(bot -> bot.state.health <= 0 && bot.active, bots)
	for b in killed_bots
		b.active = false
		b.state.note = "<dead>"
	end
	world = Dict()
	world["name"] = WORLD_NAME
	world["bots"] = [b.state for b in bots]
	s = JSON.json(world)
	debug_println(s)
	publish(conn, WORLD_NAME, JSON.json(world))
	sleep(0.1)
end
