import pygame
import math
import game_object
import Vector2D
import constants

from game_object import *
from Vector2D import *
from constants import *

class Bullet(GameObject):
    rotation = 0.0
    ready_to_spawn = True
    def __init__(self, imageFileName, initPosition, initVelocity):
        super().__init__(imageFileName, False, initPosition)
        self.velocity = initVelocity.Copy()
        self.location = initPosition.Copy()

    def Reset(self):
        self.location = Vector2D(-1000.0, -1000.0)
        self.velocity = Vector2D(0.0, 0.0)
        
    def Move(self):
        super().Move()
        if self.location.x < 0:
             return True
                    
        elif self.location.x > WIDTH:
             return True
                    
        if self.location.y < 0:
             return True
            
        elif self.location.y > HEIGHT:
             return True

    # def whatever(self):
    #     if (bullet.location.x > WIDTH - bullet.rect.width):
    #             bullets.remove(bullet)
    #             print("Bullet went off the screen")
    #         if (bullet.location.y > HEIGHT - bullet.rect.height):
    #             bullets.remove(bullet)
    #             print("Bullet went off the screen")

    #         if asteroid.CheckCollision(bullet):
    #             print("You destroyed an asteroid!")