import redis
import time
from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_bool("mock", False, "Whether to use mock sensor values")
flags.DEFINE_integer("redis_port", 6379, "Port (on localhost) for redis-server")

def get_sensor_value():
  return time.time()


redis_conn = None


def get_redis():
  global redis_conn
  if not redis_conn:
    redis_conn = redis.Redis(host='localhost', port=FLAGS.redis_port, db=0)
  return redis_conn


def listen():
  while True:
    current_value = get_sensor_value()
    get_redis().set("sensor", current_value)


def main(argv):
  print("Amber sensors.py running. Listening now...")
  listen()


if __name__ == "__main__":
  app.run(main)

