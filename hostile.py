from entity import *
from item import *


class Hostile(Entity):
	def __init__(self, pos, vel, radius, health, vision, gun):
		super().__init__(pos, vel, radius, health)
		self._vision = vision
		self._gun = gun

	# Check if player is in range
	def inRange(self, player):
		# Check distance to player
		return math.sqrt((self._posX-player.posX)**2+(self._posY-player.posY)**2) <= self._vision

	# Follows player after it comes within range
	def pursuit(self, player):
		pass

	@property
	def gun(self):
		return self._gun
	