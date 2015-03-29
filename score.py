import pygame

class Score():
	def __init__(self, startScore):
		self.score = startScore

	def addPoints(self):
		self.score += 1000

	def subtractPoints(self):
		if self.score >= 1000:
			self.score -= 1000