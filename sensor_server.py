import redis
import time
from absl import app
from absl import flags

from time_sensor import TimeSensor

FLAGS = flags.FLAGS

flags.DEFINE_bool("mock", False, "Whether to use mock sensor values")
flags.DEFINE_integer("redis_port", 6379, "Port (on localhost) for redis-server")

# Add new sensors here, as "name": SensorProcessSubclass
SENSORS = {
  "time": TimeSensor
}

redis_pool = None


def get_redis_pool():
  global redis_pool
  if not redis_pool:
    redis_pool = redis.ConnectionPool(host='localhost', port=FLAGS.redis_port, db=0)
  return redis_pool


def main(argv):
  print("Amber sensors.py running. Starting listeners.")
  pool = get_redis_pool()
  for name, sensor_class in SENSORS.items():
    sensor_process = sensor_class(name)
    print("Starting {}".format(name))
    sensor_process.start(pool)
  while True:
    # So the main process doesn't exit (which would kill the subprocesses).
    # The other way to handle this would be to launch each SensorProcess with
    # daemon=True, but then we couldn't kill them by ctrl-c'ing the main
    # process.
    pass


if __name__ == "__main__":
  app.run(main)
