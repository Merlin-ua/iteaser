from arduino import Arduino
import time
import pygame
import sys
pygame.init()

pygame.display.set_mode((100, 100))

device = Arduino()

A0 = False
A1 = False 
A2 = False
prev = pygame.time.get_ticks()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            device.close()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                device.forwardMotor()
            elif event.key == pygame.K_b:
                device.backwardMotor()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_f or event.key == pygame.K_b:
                    device.stopMotor()
    cur = pygame.time.get_ticks()
    if cur - prev < 8180:
        device.backwardMotor()
    elif cur - prev < 9760: 
        device.stopMotor()
    elif cur - prev < 15000:
        device.backwardMotor()
