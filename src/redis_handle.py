import time

import redis

from commons import SAW_CAT, LAST_TIME_SAW_CAT


class RedisHandle:
    def __init__(self):
        # using StrictRedis for response decoding to utf-8
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

    def set(self, key, val):
        self.r.set(key, val)

    def get(self, key):
        return self.r.get(key)


if __name__ == '__main__':
    # for dev only
    r = RedisHandle()

    print("checking if cats were saw...")
    # keep checking Redis to see if cat was detected
    while True:
        print(r.get(SAW_CAT))
        print(r.get(LAST_TIME_SAW_CAT))
        time.sleep(1)
