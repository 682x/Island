import math


class Entity:
    def __init__(self, pos, vel, radius, health):
        self._posX, self._posY = pos
        self._velX, self._velY = vel
        self._radius = radius
        self._health = health
        self._isDead = False

    # Collision check
    def collidesWith(self, other):
        deltaX = other.posX - self._posX
        deltaY = other.posY - self._posY
        distanceBetweenCenters = math.sqrt(deltaX ** 2 + deltaY ** 2)
        return distanceBetweenCenters < self._radius + other.radius

    def takeDamage(self, projectile):
        if self.collidesWith(projectile):
            self._health -= projectile.damage
        self._isDead = (self._health <= 0)

    # Change in velocity of self as a result of collision
    def collisionResultant(self, other):
        if not self.collidesWith(other):
            return (0, 0)
        deltaX = self._posX - other.posX
        deltaY = self._posY - other.posY
        # Push back in opposite direction
        scalar = 100 / math.sqrt(deltaX ** 2 + deltaY ** 2)
        return (deltaX * scalar, deltaY * scalar)

    # Position of entity center
    @property
    def posX(self):
        return self._posX

    @posX.setter
    def posX(self, value):
        self._posX = value

    @property
    def posY(self):
        return self._posY

    @posY.setter
    def posY(self, value):
        self._posY = value

    # 2-tuple packing of posX and posY
    @property
    def pos(self):
        return (self._posX, self._posY)

    @property
    def intPos(self):
        return tuple(map(int, self.pos))

    # Velocity of entity
    @property
    def velX(self):
        return self._velX

    @velX.setter
    def velX(self, value):
        self._velX = value

    @property
    def velY(self):
        return self._velY

    @velY.setter
    def velY(self, value):
        self._velY = value

    # Radius of entity
    @property
    def radius(self):
        return self._radius

    @property
    def isDead(self):
        return self._isDead
