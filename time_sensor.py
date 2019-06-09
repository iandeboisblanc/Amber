import time

from sensor_process import SensorProcess


class TimeSensor(SensorProcess):
  def run(self, redis_client):
    while True:
      current_time = time.time()
      redis_client.set(self.name, current_time)
