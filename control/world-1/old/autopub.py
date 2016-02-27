import redis
from time import sleep

config = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

r = redis.StrictRedis(**config)

if __name__ == '__main__':
    channel = "kev-channel"
    x = 1
    while True:
        #message = raw_input('Enter a message: ')
        #if message.lower() == 'exit':
        #    break
	message = "-"*x + "*" + "-"*(89-x)
        r.publish(channel, message)
        sleep(0.02)
        x = (x+1) % 90
