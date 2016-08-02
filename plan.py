import sys
import time

from arduino import Arduino
from multiprocessing import freeze_support

if __name__ == '__main__':
  freeze_support()
  device = Arduino()
  time.sleep(0.5)

  position = 0
  intervals = [3.0, 4.0, 3.0, 4.0, 3.0, 2.0, 2.0, 1.0, 4.0, 1.0, 5.0]

  cur = 0.0
  plan = []
  for i in xrange(len(intervals)):
      plan.append(cur + intervals[i])
      cur = plan[i]

  wait = False
  while True:
      h = device.getHammer()
      if h[4] == 1:
          wait = True
      if wait and h[4] == 0:
          break
      time.sleep(0.05)

  start = time.time()
  device.forwardMotor()
  while True:
      if time.time() - start > plan[position]:
          print 'reached', position, time.time() - start
          if position % 2 == 0:
              print 'stopping'
              device.stopMotor()
          else:
              print 'starting'
              device.forwardMotor()
          position += 1
          if position == len(plan):
              break
      time.sleep(0.05)
