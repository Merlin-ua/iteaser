# -*- coding: utf-8 -*-
import sys
import time

from arduino import Arduino
from multiprocessing import freeze_support

# Два наступних рядки істотні для роботи на ОС Windows.
if __name__ == '__main__':
  freeze_support()
  # Об'єкт який дає доступ до API мотора та молоточків.
  device = Arduino()
  # Комунікаційна бібліотека ігнорує дані деякий час, тому даємо їй час на ініціалізацію.
  time.sleep(0.5)
  # Розпочати рух вперед. Платформа буде їхати вперед доки ми її не зупинимо.
  state = [0] * 5
  count1 = [0] * 5
  count2 = [0] * 5
  count3 = [0] * 5
  value = [0] * 5
  while True:
      hammers = device.getHammer()
      finished = 0
      for i in range(len(hammers)):
          if state[i] == 0:
              value[i] = hammers[i]
              state[i] = 1
              count1[i] = time.time()
          elif state[i] == 1:
              if value[i] != hammers[i]:
                  count1[i] = time.time() - count1[i]
                  state[i] = 2
                  value[i] = hammers[i]
                  count2[i] = time.time()
          elif state[i] == 2:
              if value[i] != hammers[i]:
                  count2[i] = time.time() - count2[i]
                  state[i] = 3
                  value[i] = hammers[i]
                  count3[i] = time.time()
          elif state[i] == 3:
              if value[i] != hammers[i]:
                  count3[i] = time.time() - count3[i]
                  state[i] = 4
          elif state[i] == 4:
              finished += 1
      if finished == len(hammers):
          break
      ###################################
      # Гарною практикою є повернення контролю системі на деякий час.
      time.sleep(0.01)
  print count1
  print count2
  print count3
  print value
  state = 0
  current = 0
  start = device.getHammer()[current]
  while True:
      hammer = device.getHammer()[current]
      if state == 0:
          if hammer != start:
              if start == 1:
                  start = 0
              else:
                  state = 1
      elif state == 1:
          start = time.time() + max(count2[current] - 0.35, 0.0)
          state = 2
      elif state == 2:
          t = time.time()
          if t >= start:
              device.forwardMotor()
              stop = t + 0.32 * 4
              state = 3
      elif state == 3:
          if time.time() >= stop:
              device.stopMotor()
              current += 1
              if current == len(count1):
                  break
              state = 0
              start = device.getHammer()[current]
      time.sleep(0.01)
