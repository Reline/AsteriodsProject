import sys, pygame
from Vector2D import Vector2D
import math

#Useful functions not in classes:
def DistanceBetweenTwoPoints(pointA, pointB):
    vectorBetweenPoints = pointB.Subtract(pointA)
    #print("DistanceBetween Point A and Point B is ", vectorBetweenPoints.Magnitude())
    return vectorBetweenPoints.Magnitude()

#Classes
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
                self.location.x = screenWidth + self.location.x
                self.center.x = screenWidth + self.center.x

            if (self.location.x > screenWidth):
                self.location.x = self.location.x - screenWidth
                self.center.x = self.center.x - screenWidth

            if (self.location.y < 0):
                self.location.y = screenHeight + self.location.y
                self.center.y = screenHeight + self.center.y

            if (self.location.y > screenHeight):
                self.location.y = self.location.y - screenHeight
                self.center.y = self.center.y - screenHeight
                
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
            if (self.location.x > screenWidth - self.rect.width):
                draw_second_image = True
                second_image_location.x = self.location.x - screenWidth
            if (self.location.y > screenHeight - self.rect.height):
                draw_second_image = True
                second_image_location.y = self.location.y - screenHeight
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
            if (self.location.x > screenWidth - self.rect.width):
                check_second_collision = True
                second_image_center.x = self.center.x - screenWidth
            if (self.location.y > screenHeight - self.rect.height):
                check_second_collision = True
                second_image_center.y = self.center.y - screenHeight
            if (check_second_collision):
                distance = DistanceBetweenTwoPoints(second_image_center, someOtherGameObject.center)
                if (distance <= self.radius + someOtherGameObject.radius):
                    collided = True

        return collided



class Asteroid(GameObject):
    rotation = 0.0
    angular_velocity = 0.0
    def __init__(self, imageFileName, canLoop, newLocation, newVelocity, angularVelocity):
        super().__init__(imageFileName, canLoop, newLocation)
        self.velocity = newVelocity.Copy()
        self.angular_velocity = angularVelocity
    def Move(self):
        self.rotation = self.rotation + self.angular_velocity
        super().Move()
        
class Ship(GameObject):
    rotation = 0.0
    def __init__(self, imageFileName, canLoop, initPosition):
        super().__init__(imageFileName, canLoop, initPosition)

        
class Bullet(GameObject):
    image = pygame.image.load("attack.gif")
    rect = image.get_rect()
    rotation = 0.0
    ready_to_spawn = True
    def __init__(self, imageFileName, initPosition, initVelocity):
        super().__init__(imageFileName, False, initPosition)
        self.velocity = initVelocity.Copy()
        self.ready_to_spawn = True
        
    def Spawn(self, initPosition, initVelocity):
        self.location = initPosition.Copy()
        self.velocity = initVelocity.Copy()
        self.ready_to_spawn = False

    def Reset(self):
        self.location = Vector2D(-1000.0, -1000.0)
        self.velocity = Vector2D(0.0, 0.0)
        self.ready_to_spawn = True
        
    def Move(self):
        super().Move()
        if self.location.x < 0:
             self.Reset()
                    
        elif self.location.x > screenWidth:
             self.Reset()
                    
        if self.location.y < 0:
             self.Reset()
            
        elif self.location.y > screenHeight:
             self.Reset()
    



        
#Main Logic Start
pygame.init()

#The Screen
size = screenWidth, screenHeight = 640, 480
blue = pygame.Color(0, 0, 255, 0)
screen = pygame.display.set_mode(size)

theShip = Ship("ship.gif", True, Vector2D(320.0, 240.0))
asteroid1 = Asteroid("ball.gif", True, Vector2D(320.0, 0.0), Vector2D(2.8, -1.3), 3)
asteroid2 = Asteroid("ball.gif", True, Vector2D(160.0, 400.0), Vector2D(-1.8, 1.3), 2)
asteroids = [asteroid1, asteroid2]

aBullet = Bullet("attack.gif", Vector2D(-1000.0, -1000.0), Vector2D(0.0, 0.0))

keepGoing = True
clock = pygame.time.Clock()

while keepGoing:
    clock.tick(30)

    acceleration = 0.0
    eventList = pygame.event.get()

    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        acceleration = 0.2
    if key[pygame.K_DOWN]:
        acceleration = -0.2
    if key[pygame.K_LEFT]:
        theShip.rotation = theShip.rotation + 3
    if key[pygame.K_RIGHT]:
        theShip.rotation = theShip.rotation -3
    if key[pygame.K_SPACE]:
        if (aBullet.ready_to_spawn):
            initSpeed = 30.0
            # Calculate the bullet's velocity vector!
            bulletVelocity = Vector2D.CreateFromPolarCoordinates(initSpeed, theShip.rotation)
            bulletVelocity = bulletVelocity.Add(theShip.velocity)
            aBullet.Spawn(theShip.center, bulletVelocity)
        
    
    for event in eventList:
        if event.type == pygame.QUIT:
            keepGoing = False            
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            keepGoing = False

    # Calculate the player's ship's new velocity
    accelerationVector = Vector2D.CreateFromPolarCoordinates(acceleration, theShip.rotation)
    theShip.velocity = theShip.velocity.Add(accelerationVector)

    # Limit the ship's speed to 5
    if (theShip.velocity.Magnitude() > 5.0):
        theShip.velocity = theShip.velocity.Normalize()
        theShip.velocity = theShip.velocity.Scale(5.0)
    theShip.Move()

    # Asteroid movement & collision checks
    for an_asteroid in asteroids:
        an_asteroid.Move()
        collided_with_ship = False
        collided_with_ship = an_asteroid.CheckCollision(theShip)
        if (collided_with_ship):
            print("Player is DEAD!")
            # TODO: Do logic for re-spawning the player

    # TODO: Do bullet movement and collision check    

    screen.fill(blue)
    theShip.DrawRotatedSprite(screen, theShip.rotation)
    for an_asteroid in asteroids:
        an_asteroid.DrawRotatedSprite(screen, an_asteroid.rotation)
        
    aBullet.Move()
    aBullet.DrawRotatedSprite(screen, aBullet.rotation)
    pygame.display.flip()


#exit cleanly
pygame.quit()
