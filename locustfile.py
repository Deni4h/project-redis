from locust import User, task, between
import redis
import random
import string

# Helper untuk random string
def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class RedisClient:
    def __init__(self, environment, host='localhost', port=6379):
        self.r = redis.Redis(host=host, port=port)
        self.environment = environment

    def write(self):
        key = f"key:{random_string(5)}"
        value = random_string(20)
        try:
            with self.environment.events.request.fire(
                request_type="redis",
                name="write",
                response_time=0,  # default, nanti dihitung manual
                response_length=0,
                exception=None
            ):
                self.r.set(key, value)
        except Exception as e:
            self.environment.events.request.fire(
                request_type="redis",
                name="write",
                response_time=0,
                response_length=0,
                exception=e
            )

    def read(self):
        key = f"key:{random_string(5)}"
        try:
            with self.environment.events.request.fire(
                request_type="redis",
                name="read",
                response_time=0,
                response_length=0,
                exception=None
            ):
                self.r.get(key)
        except Exception as e:
            self.environment.events.request.fire(
                request_type="redis",
                name="read",
                response_time=0,
                response_length=0,
                exception=e
            )

class RedisUser(User):
    wait_time = between(0.001, 0.01)

    def on_start(self):
        self.client = RedisClient(environment=self.environment, host="localhost", port=6379)

    @task(2)
    def write_task(self):
        self.client.write()

    @task(1)
    def read_task(self):
        self.client.read()
