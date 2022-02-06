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
    print(r.set('foo', 'bar'))
    print(r.get('foo'))

    print(r.set('some_bool_key', 'true'))
    print(r.get('some_bool_key'))
