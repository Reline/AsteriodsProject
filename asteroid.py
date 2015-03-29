import pygame
import math
import game_object
import Vector2D
import constants

from game_object import *
from Vector2D import *
from constants import *

class Asteroid(GameObject):
    rotation = 0.0
    angular_velocity = 0.0
    def __init__(self, imageFileName, canLoop, newLocation, newVelocity, angularVelocity):
        super().__init__(imageFileName, canLoop, newLocation)
        self.velocity = newVelocity.Copy()
        self.angular_velocity = angularVelocity
        self.inSpawn = False
    def Move(self):
        self.rotation = self.rotation + self.angular_velocity
        super().Move()

    def getInSpawn(self):
        if (DistanceBetweenTwoPoints(self.center, SPAWNPOINT)) < 200:
            self.inSpawn = True
        return self.inSpawn