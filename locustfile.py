from locust import User, task, between
import redis
import random
import string
import time
import os
import hvac
from dotenv import load_dotenv

# Helper untuk random string
def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Loading environment
load_dotenv()
vault_url = os.getenv("VAULT_ADDRESS")
vault_token = os.getenv("VAULT_TOKEN")

# Menghubungkan ke Vault dan ambil password Redis
vault = hvac.Client(url=vault_url, token=vault_token)
secret = vault.secrets.kv.v1.read_secret(path='redis')
redis_pass = secret['data']['password_redis']

class RedisClient:
    def __init__(self, environment, host='localhost', port=6379, password=None):
        self.r = redis.Redis(host=host, port=port, password=password)
        self.environment = environment

    def write(self):
        key = f"key:{random_string(5)}"
        value = random_string(20)
        start_time = time.time()
        try:
            self.r.set(key, value)
            total_time = (time.time() - start_time) * 1000  # dalam ms
            self.environment.events.request.fire(
                request_type="redis",
                name="write",
                response_time=total_time,
                response_length=len(value),
                exception=None
            )
        except Exception as e:
            total_time = (time.time() - start_time) * 1000
            self.environment.events.request.fire(
                request_type="redis",
                name="write",
                response_time=total_time,
                response_length=0,
                exception=e
            )

    def read(self):
        key = f"key:{random_string(5)}"
        start_time = time.time()
        try:
            value = self.r.get(key)
            response_length = len(value) if value else 0
            total_time = (time.time() - start_time) * 1000
            self.environment.events.request.fire(
                request_type="redis",
                name="read",
                response_time=total_time,
                response_length=response_length,
                exception=None
            )
        except Exception as e:
            total_time = (time.time() - start_time) * 1000
            self.environment.events.request.fire(
                request_type="redis",
                name="read",
                response_time=total_time,
                response_length=0,
                exception=e
            )

class RedisUser(User):
    wait_time = between(0.001, 0.01)

    def on_start(self):
        self.client = RedisClient(environment=self.environment, host="localhost", port=6379, password=redis_pass)

    @task(2)
    def write_task(self):
        self.client.write()

    @task(1)
    def read_task(self):
        self.client.read()
