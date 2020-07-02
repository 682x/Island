import math
from entity import *


class Projectile(Entity):
    def __init__(self, pos, vel, radius, range, damage):
        super().__init__(pos, vel, radius, -1)
        self._range = range
        self._initPosX, self._initPosY = pos
        self._damage = damage

    # Advance the entity by a timestep, given in seconds
    def advance(self, timestep):
        self._posX += timestep * self._velX
        self._posY += timestep * self._velY
        return self

    # Check if the entity is still in range
    def inRange(self):
        deltaX = self._posX - self._initPosX
        deltaY = self._posY - self._initPosY
        distanceTravelled = math.sqrt(deltaX ** 2 + deltaY ** 2)
        return distanceTravelled <= self._range

    @property
    def range(self):
        return self._range

    @range.setter
    def velY(self, value):
        self._range = value

    @property
    def damage(self):
        return self._damage
