import time

import redis


class RedisHandle:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def set(self, key, val):
        self.r.set(key, val)

    def get(self, key):
        return self.r.get(key)


if __name__ == '__main__':
    # for dev only
    r = RedisHandle()

    # keep checking Redis to see if cat was detected
    while True:
        print("checking if cats were saw...")
        print(r.get('saw_cat'))
        time.sleep(1)
