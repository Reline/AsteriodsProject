import sys, pygame
import math
import Vector2D
import constants

from Vector2D import *
from constants import *

class GameObject(pygame.sprite.Sprite):
    rotation = 0.0
    radius = 0.0
    can_loop = True
    def __init__(self, imageFileName, canLoop, initPosition):
        self.image = pygame.image.load(imageFileName)
        self.rect = self.image.get_rect()
        if (self.rect.width > self.rect.height):
            self.radius = self.rect.width / 2.0
        else:
            self.radius = self.rect.height / 2.0
        self.can_loop = canLoop

        #location, velocity and center are all Vector2D type
        self.location = initPosition.Copy()
        self.velocity = Vector2D(0.0, 0.0)
        self.center = self.location.Add(Vector2D(self.rect.width / 2.0, self.rect.height / 2.0))
        
    
    def Move(self):
        #Calculate our new location based on our velocity and find our new center
        self.location = self.location.Add(self.velocity)
        self.center = self.center.Add(self.velocity)

        if (self.can_loop):
            #Check to see if we're going off of the edge of the screen.  If so, loop around to the other side
            if (self.location.x < 0):
                self.location.x = WIDTH + self.location.x
                self.center.x = WIDTH + self.center.x

            if (self.location.x > WIDTH):
                self.location.x = self.location.x - WIDTH
                self.center.x = self.center.x - WIDTH

            if (self.location.y < 0):
                self.location.y = HEIGHT + self.location.y
                self.center.y = HEIGHT + self.center.y

            if (self.location.y > HEIGHT):
                self.location.y = self.location.y - HEIGHT
                self.center.y = self.center.y - HEIGHT
                
    def DrawRotatedSprite(self, targetSurface, rotation):
        #refresh the image, or it will be irreversibly degraded by the rotation
        new_image = pygame.transform.rotate(self.image, rotation)
        rotated_rect = new_image.get_rect()
        clipped_rect = pygame.Rect(
            (self.rect.width - rotated_rect.width) / 2,
            (self.rect.height - rotated_rect.height) / 2,
            self.rect.width,
            self.rect.height)
        image_rect = clipped_rect.copy()
        image_rect = image_rect.move(self.location.ToList())
        targetSurface.blit(new_image, image_rect)

        #draw a second image if this image is going over the edge
        if (self.can_loop):
            draw_second_image = False
            #copy the second_image_location, because if I set second_image_location = location,
            #any changes to second_image_location will also apply to location!
            second_image_location = self.location.Copy()
            second_image_rect = clipped_rect.copy()
            if (self.location.x > WIDTH - self.rect.width):
                draw_second_image = True
                second_image_location.x = self.location.x - WIDTH
            if (self.location.y > HEIGHT - self.rect.height):
                draw_second_image = True
                second_image_location.y = self.location.y - HEIGHT
            if (draw_second_image):
                second_image_rect = second_image_rect.move(second_image_location.ToList())
                targetSurface.blit(new_image, second_image_rect)

    def CheckCollision(self, someOtherGameObject):
        collided = False

        # Check for collision between my center and the center of the other object
        # by comparing the distance between the two and the radius of both objects
        distance = DistanceBetweenTwoPoints(self.center, someOtherGameObject.center)
        if (distance <= self.radius + someOtherGameObject.radius):
            collided = True

        # TODO: Check for collision with my center on the opposite side of
        # the screen if this image is going over the edge
        if (not collided and self.can_loop):
            check_second_collision = False
            second_image_center = self.center.Copy()
            if (self.location.x > WIDTH - self.rect.width):
                check_second_collision = True
                second_image_center.x = self.center.x - WIDTH
            if (self.location.y > HEIGHT - self.rect.height):
                check_second_collision = True
                second_image_center.y = self.center.y - HEIGHT
            if (check_second_collision):
                distance = DistanceBetweenTwoPoints(second_image_center, someOtherGameObject.center)
                if (distance <= self.radius + someOtherGameObject.radius):
                    collided = True

        return collided