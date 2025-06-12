import redis

# Connect ke HAProxy
r = redis.Redis(host='localhost', port=7000)

# Test write
for i in range(5):
    key = f"user:{i}"
    value = f"deni_{i}"
    r.set(key, value)
    print(f"SET {key} -> {value}")

# Test read
for i in range(5):
    key = f"user:{i}"
    value = r.get(key)
    print(f"GET {key} -> {value.decode() if value else 'None'}")
