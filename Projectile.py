import pygame
import math


class Projectile:
    def __init__(self, x, y, radius, vx, vy, range):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx
        self.vy = vy
        self.range = range
        self.distanceTravelled = 0

    def getCoords(self):
        return (int(self.x), int(self.y))

    def getRadius(self):
        return self.radius

    def getRange(self):
        return self.range

    def getDistanceTravelled(self):
        return self.distanceTravelled

    def updatePosition(self):
        self.x += self.vx
        self.y += self.vy
        #self.distanceTravelled += math.sqrt(self.vx*self.vx + self.vy*self.vy)