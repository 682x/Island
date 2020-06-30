import pygame
import math
import random
from projectile import *
from player import *
from item import *


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Entity Properties
PLAYER_HEALTH = 100
player = Player((100, 100), (0, 0), 10, PLAYER_HEALTH)
projectileList = []
entityList = []
entityCOUNT = 10


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

# Player speed values, in px/sec
PLAYER_SPEED = 200
PLAYER_ACCELERATION = 1
defaultGun = Item("Classic", 3, 300, 300, 25, 12, 48)
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


def fireProjectile(gun):
    # Check ammo
    if gun.canShoot():
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

def handleCollisions():
    # List of projectiles / entities that remain because they don't collide
    newProjectileList = []
    newEntityList = []
    # Global declarations
    global projectileList
    global entityList
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

def updateProjectilePositions():
    global projectileList
    projectileList = [projectile.advance(timeDeltaMs) for projectile in projectileList if projectile.inRange()]


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
    for i in range(entityCOUNT):
        entityPosX = random.randint(100, WINDOW_WIDTH)
        entityPosY = random.randint(100, WINDOW_HEIGHT)
        entity = Entity((entityPosX, entityPosY), (0, 0), random.randint(20, 60), 100)
        entityList.append(entity)

generateEntities()

while not any([event.type == pygame.QUIT for event in eventList]):
    # Get time delta in seconds
    timeDeltaMs = clock.tick() / 1000
    # Get event list
    eventList = pygame.event.get()
    if any([event.type == pygame.MOUSEBUTTONDOWN for event in eventList]):
        fireProjectile(defaultGun)
    updatePlayerPosition()
    updateProjectilePositions()
    handleCollisions()
    drawGameState()

pygame.quit()
