import redis

# Jika menggunakan password dan port yang sesuai
r = redis.Redis(host='localhost', port=6379, password='deni5656')

# Setelah itu, operasi set dan get berjalan normal
for i in range(5):
    key = f"user:{i}"
    value = f"deni_{i}"
    r.set(key, value)
    print(f"SET {key} -> {value}")

for i in range(5):
    key = f"user:{i}"
    value = r.get(key)
    print(f"GET {key} -> {value.decode() if value else 'None'}")

try:
    r.ping()
    print("✅ Password benar, connect sukses.")
except redis.AuthenticationError:
    print("❌ Password salah.")