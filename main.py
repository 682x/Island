import pygame
import math
import random
from projectile import *
from player import *
from item import *
from hostile import *
from multipledispatch import dispatch


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Entity Properties
PLAYER_HEALTH = 100
player = Player((100, 100), (0, 0), 10, PLAYER_HEALTH)
projectileList = []
entityList = []
hostileList = []
HOSTILE_COUNT = 1
ENTITY_COUNT = 5


# Event list
eventList = []

# Initialize PyGame
pygame.init()
clock = pygame.time.Clock()

# Fonts
DEBUG_FONT = pygame.font.SysFont('arial', 24)

# Crosshair cursor
pygame.mouse.set_cursor(*pygame.cursors.broken_x)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Player speed values, in px/sec
PLAYER_SPEED = 200
PLAYER_ACCELERATION = 1
defaultGun = Item("Classic", 3, 300, 300, 25, 12, 48, fireRate=200, lastShot=pygame.time.get_ticks())
PROJECTILE_SPEED = 400
PROJECTILE_DAMAGE = 25
player.velX, player.velY = 0, 0


def updatePlayerPosition():
    isPressed = pygame.key.get_pressed()

    # Movement keys accelerate player in the target direction, up to a limit
    if isPressed[pygame.K_w] and player.velY > -PLAYER_SPEED:
        player.velY -= PLAYER_ACCELERATION
    elif not isPressed[pygame.K_w] and player.velY < 0:
        player.velY += PLAYER_ACCELERATION
    if isPressed[pygame.K_a] and player.velX > -PLAYER_SPEED:
        player.velX -= PLAYER_ACCELERATION
    elif not isPressed[pygame.K_a] and player.velX < 0:
        player.velX += PLAYER_ACCELERATION
    if isPressed[pygame.K_s] and player.velY < PLAYER_SPEED:
        player.velY += PLAYER_ACCELERATION
    elif not isPressed[pygame.K_s] and player.velY > 0:
        player.velY -= PLAYER_ACCELERATION
    if isPressed[pygame.K_d] and player.velX < PLAYER_SPEED:
        player.velX += PLAYER_ACCELERATION
    elif not isPressed[pygame.K_d] and player.velX > 0:
        player.velX -= PLAYER_ACCELERATION

    player.posY += player.velY * timeDeltaMs
    player.posX += player.velX * timeDeltaMs

    # Handle reloading
    if isPressed[pygame.K_r]:
        defaultGun.reload()

@dispatch(Item) # Overloading fireProjectile
def fireProjectile(gun):
    # Check ammo
    # Check current time
    currentTime = pygame.time.get_ticks()
    if gun.canShoot(currentTime):
        gun.depleteAmmo()
        # Get current mouse position
        mouseX, mouseY = pygame.mouse.get_pos()
        deltaX = mouseX - player.posX
        deltaY = mouseY - player.posY
        # Find out how much to scale the delta by
        magnitude = math.sqrt(deltaX ** 2 + deltaY ** 2)
        scalar = gun.projSpeed / magnitude
        # Calculate projectile velocity components
        projectileVelX = deltaX * scalar + player.velX
        projectileVelY = deltaY * scalar + player.velY
        # Make a new projectile instance, and push it to the list
        projectile = Projectile((player.posX, player.posY),
                            (projectileVelX, projectileVelY), gun.projRadius, gun.projRange, gun.damage)
        projectileList.append(projectile)
        gun.lastShot = currentTime


# fireProjectile function for hostile entities (same implementation as above)
@dispatch(Hostile,Item) # Overloading fireProjectile
def fireProjectile(hostile, gun):    
    currentTime = pygame.time.get_ticks()
    if gun.canShoot(currentTime):
        gun.depleteAmmo()
        # Calculate distance to player
        deltaX = hostile.posX - player.posX
        deltaY = hostile.posY - player.posY
        magnitude = math.sqrt(deltaX ** 2 + deltaY ** 2)
        scalar = gun.projSpeed / magnitude
        projectileVelX = -deltaX * scalar + hostile.velX
        projectileVelY = -deltaY * scalar + hostile.velY
        projectile = Projectile((hostile.posX, hostile.posY),
                        (projectileVelX, projectileVelY), gun.projRadius, gun.projRange, gun.damage)
        projectileList.append(projectile)
        gun.lastShot = currentTime

    if gun.currentMag == 0 and gun.remainingAmmo > 0:
        gun.reload()

def handleCollisions():
    # List of projectiles / entities that remain because they don't collide
    newProjectileList = []
    newEntityList = []
    #newHostileList = [] (I don't know how to make collisions work between player and hostile entities)

    # Global declarations
    global projectileList
    global entityList
    #global hostileList

    # Check projectiles that collide
    for projectile in projectileList:
        if not any([projectile.collidesWith(entity) for entity in entityList]):
            newProjectileList.append(projectile)
    # Check entities that collide
    for entity in entityList:
        for projectile in projectileList:
            entity.takeDamage(projectile)

        if not entity.isDead:
            newEntityList.append(entity)
    
    # Update the global lists
    projectileList = newProjectileList
    entityList = newEntityList
    #hostileList = newHostileList

def updateProjectilePositions():
    global projectileList
    projectileList = [projectile.advance(timeDeltaMs) for projectile in projectileList if projectile.inRange()]

def updateHostileActions():
    for hostile in hostileList: 
        if hostile.inRange(player):
            fireProjectile(hostile,hostile.gun)

def drawGameState():
    # Fill the background with black
    window.fill(BLACK)
    # Draw the player
    pygame.draw.circle(window, WHITE, player.intPos, player.radius)
    # Draw the projectiles
    for projectile in projectileList:
        pygame.draw.circle(window, RED, projectile.intPos, projectile.radius)
    # Draw the entities
    for entity in entityList:
        pygame.draw.circle(window, GREEN, entity.intPos, entity.radius)
    # Draw the hostiles
    for hostile in hostileList:
        pygame.draw.circle(window, BLUE, hostile.intPos, hostile.radius)
    # Draw the FPS counter
    fpsSurface = DEBUG_FONT.render(f'{int(clock.get_fps())} FPS', False, YELLOW)
    window.blit(fpsSurface, (0, 0))
    # Draw the gun name and ammo counts
    gunName = DEBUG_FONT.render(defaultGun.name, False, WHITE)
    ammoText = str(defaultGun.currentMag) + " // " + str(defaultGun.remainingAmmo);
    ammoCounter = DEBUG_FONT.render(ammoText, False, WHITE)
    window.blit(gunName, (15, WINDOW_HEIGHT-55))
    window.blit(ammoCounter, (15, WINDOW_HEIGHT-30))
    # Update the window
    pygame.display.flip()

def generateEntities():
    for i in range(ENTITY_COUNT):
        entityPosX = random.randint(100, WINDOW_WIDTH)
        entityPosY = random.randint(100, WINDOW_HEIGHT)
        entity = Entity((entityPosX, entityPosY), (0, 0), random.randint(20, 60), 100)
        entityList.append(entity)

generateEntities()

def generateHostiles():
    for i in range(HOSTILE_COUNT):
        hostilePosX = random.randint(100, WINDOW_WIDTH)
        hostilePosY = random.randint(100, WINDOW_HEIGHT)
        hostileDefaultGun = Item("Classic", 3, 300, 300, 25, 12, 48, fireRate=500, lastShot=pygame.time.get_ticks())
        hostile = Hostile(pos=(hostilePosX, hostilePosY), vel=(0, 0), radius=10, health=100, vision=300, gun=hostileDefaultGun)
        # Don't spawn inside another entity and spawn outside of range of player
        while(any(hostile.collidesWith(entity) for entity in entityList) or any(hostile.collidesWith(other) for other in hostileList) or hostile.inRange(player)):        
            hostilePosX = random.randint(100, WINDOW_WIDTH)
            hostilePosY = random.randint(100, WINDOW_HEIGHT)
            hostile = Hostile(pos=(hostilePosX, hostilePosY), vel=(0, 0), radius=10, health=100, vision=300, gun=hostileDefaultGun)
        hostileList.append(hostile)

generateHostiles()

while not any([event.type == pygame.QUIT for event in eventList]):
    # Get time delta in seconds
    timeDeltaMs = clock.tick() / 1000
    
    # Get event list
    eventList = pygame.event.get()
    if any([event.type == pygame.MOUSEBUTTONDOWN for event in eventList]):
        fireProjectile(defaultGun)
    updatePlayerPosition()
    updateHostileActions()
    updateProjectilePositions()
    handleCollisions()
    drawGameState()

pygame.quit()
