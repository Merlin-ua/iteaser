import pygame
import sys

from arduino import Arduino
from multiprocessing import freeze_support

if __name__ == '__main__':
  freeze_support()
  device = Arduino()
  pygame.init()
  pygame.display.set_mode((100, 100))
  prev = pygame.time.get_ticks()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        device.close()
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_f:
          device.forwardMotor()
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_f:
          device.stopMotor()
    cur = pygame.time.get_ticks()
    if cur - prev > 1000:
      prev = cur
      print device.getHammer()
      print '=' * 20
