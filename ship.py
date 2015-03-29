import pygame
import math
import game_object
import Vector2D
import bullet
import constants

from game_object import *
from Vector2D import *
from bullet import *
from constants import *

class Ship(GameObject):
    rotation = 0.0
    def __init__(self, imageFileName, canLoop, initPosition):
        super().__init__(imageFileName, canLoop, initPosition)

        self.lives = 10
        self.initPosition = initPosition.Copy()

    def playerMove(self):
    	key = pygame.key.get_pressed()
    	acceleration = 0.0
    	slowFactor = 0.1

    	if key[pygame.K_UP]:
    		acceleration = 0.1
    	if key[pygame.K_DOWN]:
    		acceleration = -0.1
    	if key[pygame.K_LEFT]:
    		self.rotation = self.rotation + 5
    	if key[pygame.K_RIGHT]:
    		self.rotation = self.rotation -5
    	if not (key[pygame.K_UP] or key[pygame.K_DOWN]):
    		if self.velocity.x > 0:
    			self.velocity.x -= slowFactor
    		elif self.velocity.x < 0:
    			self.velocity.x += slowFactor
    		if self.velocity.y > 0:
    			self.velocity.y -= slowFactor
    		elif self.velocity.y < 0:
    			self.velocity.y += slowFactor

    	#Calculate the player's ship's new velocity
    	accelerationVector = Vector2D.CreateFromPolarCoordinates(acceleration, self.rotation)
    	self.velocity = self.velocity.Add(accelerationVector)

    	# Limit the ship's speed to 5
    	if (self.velocity.Magnitude() > 7.0):
    		self.velocity = self.velocity.Normalize()
    		self.velocity = self.velocity.Scale(5.0)
    	self.Move()

    def shoot(self):
    	initSpeed = 15.0
    	# Calculate the bullet's velocity vector!
    	bulletCalculate = Vector2D.CreateFromPolarCoordinates(initSpeed, self.rotation)
    	bulletVelocity = bulletCalculate.Add(self.velocity)

    	bullet = Bullet("attack.gif", self.center, bulletVelocity)

    	return bullet

    def loseLife(self):
    	playerIsAlive = True

    	if self.lives > 0:
            self.lives -= 1
            if self.lives <= 0:
                playerIsAlive = False
            else:
                return playerIsAlive

    def respawn(self):
        self.location = self.initPosition
        self.center = self.location.Add(Vector2D(self.rect.width / 2.0, self.rect.height / 2.0))
        self.rotation = 0.0
        self.velocity.x = 0.0
        self.velocity.y = 0.0