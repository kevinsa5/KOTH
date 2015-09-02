#!/usr/bin/julia

using Redis, JSON

conn = RedisConnection()

t = 0
while true
	publish(conn, "kev-channel", JSON.json(Dict("x"=>(t*10)%100, "y"=>50*sin(t)+50)))
	t += 0.1
	sleep(0.1)
end
