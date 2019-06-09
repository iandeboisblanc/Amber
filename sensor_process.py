from multiprocessing import Process

import redis


class SensorProcess():
  def __init__(self, name):
    self.name = name

  def _make_target(self):
    def target(redis_conn_pool):
      redis_client = redis.Redis(connection_pool=redis_conn_pool)
      self.run(redis_client)
    return target

  def start(self, redis_conn_pool):
    """Starts the process, triggering run() to be called in subprocess."""
    target = self._make_target()
    # I think we're supposed to pass mutable resources like this?
    args = (redis_conn_pool,)
    process = Process(target=target,
                      args=args,
                      name="SensorProcess-{}".format(self.name))
    process.start()

  def run(self, redis_client):
    """Main entry point for this SensorProcess.

    Subclasses should override this with the behavior they need to continuously
    read their sensors and publish values to Redis.
    """
    raise NotImplementedError
