#!/usr/bin/julia

using Redis, JSON

conn = RedisConnection()

(so, si, pr) = readandwrite(`/usr/lib/cgi-bin/bots/bot.py`)
write(si, "KOTH Controller is Ready\n")
resp = readline(so)
if resp != "KOTH Bot is Ready\n"
	error("KOTH Bot is talking funny: " * resp)
end
println("Setup good, entering loop")
while true
	write(si,"here is a thing to read\n")
	resp = chomp(readline(so))
	println("Got this:" * resp)
	publish(conn, "kev-channel", resp)
	sleep(0.1)
end
