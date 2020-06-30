class Item:
    def __init__(self, name, projRadius, projSpeed, projRange, damage, magSize, totalAmmo):
        self._name = name
        self._projRadius = projRadius
        self._projSpeed = projSpeed
        self._projRange = projRange
        self._damage = damage
        self._magSize = magSize
        self._totalAmmo = totalAmmo
        self._currentMag = magSize
        self._remainingAmmo = totalAmmo - magSize

    def canShoot(self):
        return self._currentMag > 0

    def reload(self):
        self._remainingAmmo -= self._magSize
        self._remainingAmmo += self._currentMag
        self._currentMag = self._magSize
        if self._remainingAmmo < 0:
            self._currentMag += self._remainingAmmo
            self._remainingAmmo = 0

    def depleteAmmo(self):
        self._currentMag -= 1

    @property
    def name(self):
        return self._name

    @property
    def projRadius(self):
        return self._projRadius

    @property
    def projSpeed(self):
        return self._projSpeed

    @property
    def projRange(self):
        return self._projRange

    @property
    def damage(self):
        return self._damage

    @property
    def magSize(self):
        return self._magSize

    @property
    def totalAmmo(self):
        return self._totalAmmo

    @property
    def currentMag(self):
        return self._currentMag

    @property
    def remainingAmmo(self):
        return self._remainingAmmo
