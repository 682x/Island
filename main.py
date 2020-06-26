import pygame
import Projectile
import Player
import math


pygame.init()
windowWidth = 600
windowHeight = 600
window = pygame.display.set_mode((windowWidth, windowHeight))

playerX = 100
playerY = 100
playerRadius = 10
playerSpeed = 4
playerShots = []


def drawprojectile(proj):
    pygame.draw.circle(window, (255, 0, 0), proj.getCoords(), proj.getRadius())


running = True
while running:
    pygame.time.delay(17)
    shooting = False
    player_vx = 0
    player_vy = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            shooting = True

    keys = pygame.key.get_pressed()
    xMouse, yMouse = pygame.mouse.get_pos()
    if keys[pygame.K_w] and playerY > playerSpeed+playerRadius:
        playerY -= playerSpeed
        player_vy -= playerSpeed
    if keys[pygame.K_a] and playerX > playerSpeed+playerRadius:
        playerX -= playerSpeed
        player_vx -= playerSpeed
    if keys[pygame.K_s] and playerY < windowHeight-playerSpeed-playerRadius:
        playerY += playerSpeed
        player_vy += playerSpeed
    if keys[pygame.K_d] and playerX < windowWidth-playerSpeed-playerRadius:
        playerX += playerSpeed
        player_vx += playerSpeed

    if shooting:
        print("shooting")
        #pygame.draw.circle(window, (255, 255, 255), (xMouse, yMouse), 12)
        dx = xMouse-playerX
        dy = yMouse-playerY
        v = 5
        magnitude = math.sqrt(dx*dx + dy*dy)
        # massFactor dictates how much of the players velocity is transferred to the bullet
        massFactor = 1.0/3
        # player momentum is carried along to the bullet
        shot = Projectile.Projectile(playerX, playerY, 4, v*dx/magnitude+player_vx*massFactor, v*dy/magnitude+player_vy*massFactor, 300)
        playerShots.append(shot)

    window.fill((0, 0, 0))
    pygame.draw.circle(window, (255, 255, 255), (playerX, playerY), playerRadius)
    for i in range(len(playerShots)):
        drawprojectile(playerShots[i])
        playerShots[i].updatePosition()
        #if playerShots[i].getDistanceTravelled() > playerShots[i].getRange():
        #    playerShots.pop(i)
    pygame.display.update()

pygame.quit()
print(playerShots)