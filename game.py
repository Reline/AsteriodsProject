import sys, pygame, random, math
import ship
import asteroid
import game_object
import bullet
import constants
import score

from random import randint
from ship import *
from asteroid import *
from game_object import *
from bullet import *
from Vector2D import *
from constants import *
from score import *

def main():

	pygame.init()

	ship = Ship("player.png", True, SPAWNPOINT)
	background = pygame.image.load("img/background.jpeg").convert_alpha()
	numberOfAsteroids = 0
	asteroidList = []
	bulletList = []
	score = Score(0)

	gameIsRunning = True

	clock = pygame.time.Clock()

	while gameIsRunning:

	################################### START INTRO SCREEN LOOP #####################################
		introScreen = False
		if gameIsRunning:
			introScreen = True

		while introScreen:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						introScreen = False
					elif event.key == pygame.K_ESCAPE:
						gameIsRunning = False
						pygame.init()
						introScreen = False
				elif event.type == pygame.QUIT:
					gameIsRunning = False
					pygame.init()
					introScreen = False

			titleText = GAMEFONT.render("Welcome to ASTEROIDS!", True, WHITE)
			titleRect = titleText.get_rect()
			#change rect center for blitting
			titleLocation = titleRect.centerx, titleRect.centery = WIDTH/2, HEIGHT/2

			pressSpace = GAMEFONT.render("Press the spacebar to begin.", True, RED)
			pressRect = pressSpace.get_rect()
			pressSpaceLocation = pressRect.centerx, pressRect.top = WIDTH/2, HEIGHT/2

			SCREEN.blit(background, (0,0))
			SCREEN.blit(titleText, (WIDTH/2 - titleRect.width/2, HEIGHT/2 - titleRect.height/2))
			SCREEN.blit(pressSpace, (WIDTH/2 - titleRect.width/2, HEIGHT/2 + titleRect.height))


			pygame.display.flip()

		mainGameLoop = False
		if gameIsRunning:
			mainGameLoop = True

	##################################### END INTRO SCREEN LOOP ######################################

	##################################### START MAIN GAME LOOP #######################################

		while mainGameLoop:
			clock.tick(30)
			acceleration = 0.0
			eventList = pygame.event.get()
			key = pygame.key.get_pressed()

			ship.playerMove()

			for event in eventList:
				if key[pygame.K_SPACE]:
					if len(bulletList) < 15:
						bullet = ship.shoot()
						bulletList.append(bullet)

			for bullet in bulletList:
				offScreen = bullet.Move()
				if offScreen:
					bulletList.remove(bullet)
					#print("A bullet went off the screen")
				for asteroid in asteroidList:
					destroyedAsteroid = bullet.CheckCollision(asteroid)
					if destroyedAsteroid:
						#DESTROY ASTEROID
						score.addPoints()
						asteroidList.remove(asteroid)
						numberOfAsteroids -= 1
						# print("An asteroid has been destroyed")


			for event in eventList:
				if event.type == pygame.QUIT:
					# print(score.score)
					gameIsRunning = False
					pygame.init()
					mainGameLoop = False            
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					# print(score.score)
					gameIsRunning = False
					pygame.init()
					mainGameLoop = False


			#asteroid spawning
			if numberOfAsteroids < 25:
				noAsteroid = True
				while noAsteroid:
					asteroidXDirection = randint(0,1)
					if asteroidXDirection == 0:
						asteroidXDirection = -1
					asteroidYDirection = randint(0,1)
					if asteroidYDirection == 0:
						asteroidYDirection = -1
					asteroid = Asteroid("asteroid" + str(randint(1,5)) + ".png", True, Vector2D(randint(0, WIDTH), randint(0, HEIGHT)), Vector2D(randint(1,7)*asteroidXDirection, randint(1, 7)*asteroidYDirection), randint(-3,3))
					if asteroid.CheckCollision(ship):
						noAsteroid = True
					elif 200 > DistanceBetweenTwoPoints(asteroid.center, ship.center):
						noAsteroid = True
					else:
						noAsteroid = False
				asteroidList.append(asteroid)
				numberOfAsteroids += 1

			# Asteroid movement & collision checks
			for asteroid in asteroidList:
				asteroid.Move()

				asteroidInSpawn = False

				collided_with_ship = False
				collided_with_ship = asteroid.CheckCollision(ship)

				if (collided_with_ship):
					score.subtractPoints()
					asteroidList.remove(asteroid)
					numberOfAsteroids -= 1
					mainGameLoop = ship.loseLife()
					for asteroid in asteroidList:
						asteroidInSpawn = asteroid.getInSpawn
						if asteroidInSpawn:
							asteroidList.remove(asteroid)
							numberOfAsteroids -= 1
					ship.respawn()
						
						

			# TODO: Do logic for re-spawning the player

			SCREEN.blit(background, (0,0))
			ship.DrawRotatedSprite(SCREEN, ship.rotation)
			for asteroid in asteroidList:
				asteroid.DrawRotatedSprite(SCREEN, asteroid.rotation)
			for bullet in bulletList:
				bullet.DrawRotatedSprite(SCREEN, bullet.rotation)

			scoreText = GAMEFONT.render('Score: ' + str(score.score), True, WHITE)
			scoreRect = scoreText.get_rect()
			playerLives = GAMEFONT.render('Lives: ' + str(ship.lives), True, WHITE)
			livesRect = playerLives.get_rect()
			SCREEN.blit(scoreText, (0, 0))
			SCREEN.blit(playerLives, (WIDTH - livesRect.width, 0))

			pygame.display.flip()

	############################## END MAIN GAME LOOP ###################################

	############################# START GAME OVER SCREEN LOOP ###########################

		gameOver = False
		if gameIsRunning:
			gameOver = True

		while gameOver:
			endText = bigGAMEFONT.render("GAME OVER", True, WHITE)
			endTextRect = endText.get_rect()
			#change rect center for blitting
			endTextLocation = endTextRect.centerx, endTextRect.centery = WIDTH/2, HEIGHT/2

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						main()
					elif event.key == pygame.K_ESCAPE:
						gameOver = False
				elif event.type == pygame.QUIT:
					gameOver = False

			SCREEN.blit(background, (0,0))
			SCREEN.blit(endText, (WIDTH/2 - endTextRect.width/2, HEIGHT/2 - endTextRect.height/2))
			SCREEN.blit(scoreText, (0,0))
			pygame.display.flip()

		gameIsRunning = False

	############################# END GAME OVER SCREEN LOOP ##############################

	#exit cleanly
	pygame.quit()

main()
