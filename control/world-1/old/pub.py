import redis

config = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

r = redis.StrictRedis(**config)

if __name__ == '__main__':
    channel = "kev-channel"
    while True:
        message = raw_input('Enter a message: ')
        if message.lower() == 'exit':
            break
        message = '{message}'.format(**locals())
        r.publish(channel, message)

