import pgzrun
import pygame
from pygame.locals import *
import random
from random import randint
import time
from time import sleep
from pgzhelper import *
import math

WIDTH = 612
HEIGHT = 612

game_over = False
wave = 0

ship = Actor("spaceship")
ship.x = 306
ship.y = 550
ship.angle = 180

playerbullets = []
playerbullet_timeout = False
playerbullet_ticks = 0

hp = 10
score = 0

enemy_bullets = []
for _ in range(5):
  enemy_bullets.append(Actor("enemylaser"))

choose_enemy_bullet = []
for _ in range(5):
  choose_enemy_bullet.append(random.randint(1,8))

bullet_start = [False, False, False, False]

random_bullets = []
for _ in range(5):
  random_bullets.append(random.randint(800,1300))

axenemies = []
for i in range(15):
  enemy = Actor("pixelstarshipenemy1")
  enemy.x = 60 + (i % 8) * 70 + math.floor(i / 8) * 35
  enemy.y = 60 + (math.floor(i / 8) * 50)
  axenemies.append(enemy)

enemies_defeated = [0,0,0]

enemyboss = Actor("pixelenemyboss")
enemyboss.scale = 0.45
enemyboss.angle = 180
enemyboss.x = 306
enemyboss.y = 6000
enemybossHP = 10

boss_bullets = []

for i in range(3):
  boss_bullet = Actor("redbulletbill")
  boss_bullet.scale = 0.2
  boss_bullet.angle = (random.randint(-130, -50))
  boss_bullet.x = -1000
  boss_bullets.append(boss_bullet)

random_boss_bullets = []
for i in range(3):
  random_boss_bullets.append(random.randint(800,1200))

enemybosses = []
enemybosses.append(enemyboss)

background = Actor("pixelstarbackground")
background.y = -306

shields = []
shield_HP = []
for x in range(2):
  shield = Actor("shield")
  shield.scale = 0.5
  shield.x = 150 + (300 * x)
  shield.y = 490
  shields.append(shield)
  shield_HP.append(15)
heart = Actor("heart") #powerups // extra heart
heart.scale = 0.05
heart.x = 30
heart.y = 50
hearts = []
hearts.append(heart)

extraheart = Actor("heartpickup")
extraheart.x = 3000
extraheart.y = 3000
extraheart.scale = 0.12
extrahearts = []
extrahearts.append(extraheart)

game_start_ticks = 0
game_state = 11
game_state_12_start = 1

new_wave_ticks = 0
new_wave = 0

boss_wave_ticks = 0
boss_wave = False
boss_wave_start = 0

extraheart_ticks = 0
extraheart_start = 1
extraheart_collected = False

gameoverscreen = Actor("gameover")
gameoverscreen.x = 306
gameoverscreen.y = 306
winscreen = Actor("winscreen")
winscreen.x = 306
winscreen.y = 306

def update():
  global score, game_over, hp, choose_enemy_bullet, game_start_ticks, game_state, bullet_start, boss_bullets, random_bullets, playerbullet_timeout, playerbullet_ticks, enemies_defeated, game_state_12_start, new_wave_ticks, new_wave, boss_wave_ticks, boss_wave, boss_wave_start, extraheart_ticks, extraheart_start, extraheart_collected, shields, enemybossHP, random_boss_bullets
 
  if extraheart_ticks >= 2500 and extraheart_start == 1:
    extraheart.x = (random.randint(40, 600))
    extraheart.y = -400
    extraheart_start = 0
    
  elif extraheart_start == 0:
    extraheart.y += 6
  else:
    extraheart_ticks += 1

  if ship.collidelist(extrahearts) != -1 and extraheart_collected == False:
    extraheart.y = 5000
    extraheart_collected = True
    hp += 1
 
  if game_state == 11:
    game_start_ticks += 1
  if game_start_ticks >= 250:
    bullet_start[0] = True
  if game_start_ticks >= 600:
    bullet_start[1] = True
    
  if game_start_ticks >= 750:
    bullet_start[2] = True
    
  if game_start_ticks >= 1000:
    bullet_start[3] = True

  if enemies_defeated[0] == 15:
    new_wave = 1
    if new_wave == 1:
      new_wave_ticks += 1
    if new_wave_ticks >= 300:
      enemies_defeated[0] = 0
      game_state = 12
      new_wave_ticks = 0
      new_wave = 0

  if game_state == 12 and game_state_12_start == 1:#level1_wave2
    for i in range(15):
      axenemies[i].y = 60 + (math.floor(i / 8) * 50)
    game_state_12_start = 0
  
  if enemies_defeated[1] == 15:
    boss_wave_ticks += 1
    if boss_wave_ticks >= 300:
      enemies_defeated[1] = 0
      game_state = 13
      boss_wave_ticks = 0
      boss_wave = True
      boss_wave_start = 1

  if game_state == 13 and boss_wave_start == 1:#level1_wave3
    for i in range(6):
        axenemies[i].x = 60 + 70 * i + math.floor((i + 7) / 10) * 140
        axenemies[i].y = 60
        axenemies[i + 6].x = 60 + 70 * i + math.floor((i + 7) / 10) * 140
        axenemies[i + 6].y = 110

    enemyboss.x = 308
    enemyboss.y = 90
    boss_wave_start = 0
 
  if keyboard.a and ship.x >= 0 or keyboard.left and ship.x >= 0: # ship movement
    ship.x = ship.x - 4
  if keyboard.d and ship.x <= 612 or keyboard.right and ship.x <= 612:
    ship.x = ship.x + 4
  if keyboard.s and ship.y <= 612 or keyboard.down and ship.y <= 612:
    ship.y = ship.y + 4
  if keyboard.w and ship.y >= 300 or keyboard.up and ship.y >= 300:
    ship.y = ship.y - 4
  
  if playerbullet_timeout == True: # ship shoot timeout
    playerbullet_ticks += 1
  if playerbullet_ticks >= 50:
    playerbullet_timeout = False

  if keyboard.space and playerbullet_timeout == False:
    playerbullet = Actor("playerlaser")
    playerbullet.angle = 90
    playerbullets.append(playerbullet)
    playerbullet.x = ship.x
    playerbullet.y = ship.y
    
    playerbullet_timeout = True
    playerbullet_ticks = 0

  for playerbullet in playerbullets: #bullet remove
    playerbullet.y -= 5
    if playerbullet.y <= -50:
      playerbullets.remove(playerbullet)

    for i in range(15):
      if playerbullet.collidelist([axenemies[i]]) != -1:
        score += 10
        enemies_defeated[0] += 1
        playerbullets.remove(playerbullet)
        axenemies[i].y = 1000
        if game_state == 12:
          enemies_defeated[1] += 1
        if boss_wave:
          enemies_defeated[2] += 1
      
    if playerbullet.collidelist(enemybosses) != -1: #boss
      playerbullet.y = 1000
      playerbullets.remove(playerbullet)
      enemybossHP -= 1
      if enemybossHP <= 0:
        enemyboss.y = 2000
        score += 1000
    
    if playerbullet.collidelist([shields[0]]) != -1: #shields kan ikke bli skutt gjennom av spiller
      playerbullet.y = 3000
      playerbullets.remove(playerbullet)
      shield_HP[0] -= 1
    if playerbullet.collidelist([shields[1]]) != -1:
      playerbullet.y = 3000
      playerbullets.remove(playerbullet)
      shield_HP[1] -= 1
    
  def noe_bullets(i):
    enemy_bullets[i].x = axenemies[choose_enemy_bullet[i]-1].x
    enemy_bullets[i].y = axenemies[choose_enemy_bullet[i]-1].y
    choose_enemy_bullet[i] = 0
  for i in range(5):
    if choose_enemy_bullet[i] > 0:
      noe_bullets(i)

    enemy_bullets[i].y = enemy_bullets[i].y + 5

    if enemy_bullets[i].y >= random_bullets[i]:
      choose_enemy_bullet[i] = (random.randint(1,15))
      random_bullets[i] = (random.randint(800,1300))

    if enemy_bullets[i].collidelist([shields[0]]) != -1: #shields
      shield_HP[0] -= 1
      noe_bullets(i)
    elif enemy_bullets[i].collidelist([shields[1]]) != -1:
      shield_HP[1] -= 1
      noe_bullets(i)

  def noe_boss():
    boss_bullets[i].x = enemyboss.x
    boss_bullets[i].y = enemyboss.y
    boss_bullets[i].angle = (random.randint(-130, -50))
    random_boss_bullets[i] = (random.randint(800,1100))

  for i in range(3):
    if boss_wave:
      boss_bullets[i].move_forward(4)
      if boss_bullets[i].y >= random_boss_bullets[i] or boss_bullets[i].x > 700 or boss_bullets[i].x < -100:
        noe_boss()

  for i in range(3):
    if ship.collidelist([boss_bullets[i]]) != -1:
      noe_boss()
      hp -= 1

  for i in range(3):
    if boss_bullets[i].collidelist([shields[0]]) != -1:
      shield_HP[0] -= 1
      noe_boss()
    elif boss_bullets[i].collidelist([shields[1]]) != -1:
      shield_HP[1] -= 1
      noe_boss()
   
  for i in range(5): #bullet collide
    if ship.collidelist([enemy_bullets[i]]) != -1 and hp > 0:
      choose_enemy_bullet[i] = (random.randint(1,15))
      hp -= 1

  if hp == 0: #game over
    game_over = True
    game_state = 0
    boss_wave = False
  if enemybossHP <= 0 and enemies_defeated[2] == 12:
    hp = 1000
    
  background.y = background.y + 2 #background
  if background.y == 918:
    background.y = -306
  
def draw():
  if game_over:
    background.draw()
    heart.draw()
    screen.draw.text("x"+ str(hp), (50, 40), color = (255,255,255), fontsize = 30)
    screen.draw.text('Score: ' + str(score), (15,10), color = (255,255,255), fontsize = 30)
    gameoverscreen.draw()
    
  else:
    background.draw()
    ship.draw()
    
    for playerbullet in playerbullets:
      playerbullet.draw()
    
    for i in range(15):
      axenemies[i].draw()
    
    if enemybossHP > 0:
      enemyboss.draw()
      for i in range(3):
        boss_bullets[i].draw()

    for x in range(5):
      enemy_bullets[x].draw()    

    for i in range(2):
      if shield_HP[i] > 0:
        shields[i].draw()
        screen.draw.text(str(shield_HP[i]), (shields[i].x-5, shields[i].y-5), color = (0,0,0), fontsize = 25)

      elif shield_HP[0] <= 0:
        shields[i].y = 2000

    if boss_wave:
      screen.draw.text("Boss HP: "+ str(enemybossHP), (15, 70), color = (255,255,255), fontsize = 30)
      boss_bullets[0].draw()
      boss_bullets[1].draw()

    if extraheart_collected == False:
      extraheart.draw()
    
    heart.draw()
    screen.draw.text("x"+ str(hp), (50, 40), color = (255,255,255), fontsize = 30)
    screen.draw.text('Score: ' + str(score), (15,10), color = (255,255,255), fontsize = 30)

    if enemybossHP <= 0 and enemies_defeated[2] == 12:
      winscreen.draw()
      
pgzrun.go()