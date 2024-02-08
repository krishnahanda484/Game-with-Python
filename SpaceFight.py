import math
import random

import pygame
from pygame import mixer

#Initializing pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800, 600))

#Background
background = pygame.image.load('Background.png')

# Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Army")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
PlayerImg = pygame.image.load("space-invaders.png")
PlayerX = 370
PlayerY = 480
PlayerX_change = 0

#Enemy
enemyImg = []
enemyX=  []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6


for i in range(num_of_enemies):
   enemyImg.append(pygame.image.load("enemy.png"))
   enemyX.append(random.randint(0,736))
   enemyY.append(random.randint(50,150))
   enemyX_change.append(4)
   enemyY_change.append(40)

#Bullets

# Ready - Can't see the bullet pn the screen
# Fire - The bullet is currently moving

BulletImg = pygame.image.load("Bullet1.png")
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 10
Bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
testY = 10

#Game Over Text
over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x,y):
   score = font.render("Score :"+ str(score_value),True,(255,255,255))
   screen.blit(score,(x,y))

def game_over_text(x,y):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
def player(x,y):
   screen.blit(PlayerImg, (x,y))


def enemy(x,y, i):
   screen.blit(enemyImg[i],(x,y))


def fire_bullet(x,y):
   global Bullet_state
   Bullet_state = "fire"
   screen.blit(BulletImg,(x + 16,y + 10))


def isCollision(enemyX,enemyY,BulletX,BulletY):
   distance = math.sqrt(math.pow(enemyX-BulletX,2)+ math.pow(enemyY-BulletY,2))
   if distance < 27:
       return True
   else:
       return False

# Game Loop
running = True
while running:

   # RGB - Red, Green , Blue
   screen.fill((0, 0, 0))
   #Background Image
   screen.blit(background,(0, 0))
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False

   #if keystroke is pressed check whether its right or left
       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_LEFT:
               PlayerX_change = -5
           if event.key == pygame.K_RIGHT:
               PlayerX_change = 5
           if event.key == pygame.K_SPACE:
               if Bullet_state is "ready":
                   #Get the current x the coordinates of the spaceship
                   bullet_Sound = mixer.Sound('laser.wav')
                   bullet_Sound.play()
                   bulletX = PlayerX
                   fire_bullet(BulletX,BulletY)

       if event.type == pygame.KEYUP:
           if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               playerX_change = 0

#Boundaries for Player
PlayerX += PlayerX_change
if PlayerX <= 0:
    PlayerX = 0
elif PlayerX >= 736:
    PlayerX = 736

#Boundaries for Enemies
for i in range(num_of_enemies):

    #Game Over
    if enemyY[i] > 440:
        for j in range(num_of_enemies):
            enemyY[j]  = 2000
        game_over_text()
        break

    enemyX[i] += enemyX_change[i]
    if enemyX[i] <= 0:
       enemyX_change[i] = 2
       enemyY[i] += enemyY_change[i]
    elif enemyX[i] >= 736:
       enemyX_change[i] = -2
       enemyY[i] += enemyY_change[i]

   # Collion
       collision = isCollision(enemyX[i], enemyY[i], BulletX, BulletY)
       if collision:
           explosion_Sound = mixer.Sound('explosion.wav')
           explosion_Sound.play()
           BulletY = 480
           Bullet_state = "ready"
           score_value += 1
           enemyX[i] = random.randint(0, 736)
           enemyY[i] = random.randint(50, 150)

       enemy(enemyX[i], enemyY[i],i)

#  Bullet Movement
    if BulletY <= 0:
        BulletY = 480
        Bullet_state = "ready"

    if Bullet_state == "fire":
        fire_bullet(PlayerX,BulletY)
        BulletY -= BulletY_change

    player(PlayerX, PlayerY)
    show_score(textX,testY)
    pygame.display.update()

