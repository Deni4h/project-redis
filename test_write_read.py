import os
import redis
import hvac
from dotenv import load_dotenv

# 1. Loading environment variables from .env
load_dotenv()
vault_url = os.getenv("VAULT_ADDRESS")
vault_token = os.getenv("VAULT_TOKEN")

# 2. Hubungkan ke Vault
vault = hvac.Client(url=vault_url, token=vault_token)

# 3. Baca password dari Vault (KV v1)
secret = vault.secrets.kv.v1.read_secret(path='redis')
redis_pass = secret['data']['password_redis']

# 4. Setelah dapat password, connect ke Redis
r = redis.Redis(host='localhost', port=6379, password=redis_pass)

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
