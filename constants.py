import pygame
import sys
import Vector2D

from Vector2D import *

pygame.init()

GAMEFONT = pygame.font.SysFont("arial", 48)
bigGAMEFONT = pygame.font.SysFont("arial", 72)

BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)

WIDTH = 1920
HEIGHT = 1080
SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)

SPAWNPOINT = Vector2D(WIDTH/2, HEIGHT/2)