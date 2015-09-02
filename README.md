SPS King of the Hill
--------------------

A King of the Hill game for the UNC SPS.  

See http://codegolf.stackexchange.com/tags/king-of-the-hill/info

How it works, technically speaking: 

1.  A world controller, written in the Julia language, runs each bot as a subprocess and talks to it through STDIN/STDOUT.  It publishes the world data to a Redis server instance.
2.  A number of python cgi relays are subscribed to the Redis channel and send the world data to the browser through WebSocket connections.
3.  The browser runs some JS to display the world graphically.

Right now, only the julia->redis->python->browser tunnel is complete.  The world controller and the browser rendering code still need written.
