import pygame
import sys
import random
import time
import pandas as pd
import csv
from pygame.locals import *

pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()

WIDTH = 1000
HEIGHT = 600

RED = (255,0,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
YELLOW =(255,255,0)
GREEN = (124,252,0)
Threshold = 50
player_size = 50
shift_size = 40

player_pos = [WIDTH/2, HEIGHT- 2*player_size]

enemy_size = 50
enemy_pos = [random.randint(0,WIDTH-enemy_size), 0]
enemy_list = [enemy_pos]

speed = 0

screen = pygame.display.set_mode((WIDTH,HEIGHT))

game_over = False

clock = pygame.time.Clock()
clock_time = 30
start_time = time.time()

myFont = pygame.font.SysFont("monospace", 35);

# music section
pygame.mixer.music.load("jazzinparis.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

def save_data():
    fields = [name,age,score,Level]
    with open(r'Data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0,WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos,y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE ,(enemy_pos[0] , enemy_pos[1] , enemy_size , enemy_size))

def detect_collision(player_pos,enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]
    e_x = enemy_pos[0]
    e_y = enemy_pos[1]
    if (e_x>=p_x and e_x<(p_x+player_size)) or (p_x>=e_x and p_x<(e_x+enemy_size)):
        if (e_y>=p_y and e_y < (p_y+player_size)) or (p_y>=e_y and p_y<(e_y+enemy_size)):
            return True
    return False

def update_enemy_positions(enemy_list, score):
    # change enemy position
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >=0 and enemy_pos[1] <HEIGHT:
            enemy_pos[1] += speed*1.5
        else:
            enemy_list.pop(idx)
            score += 1
    return score


def collision_check(enemy_list,player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos,player_pos):
            return True
    return False

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass


def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, (0,0,0), ((screen.get_width() / 2) - 100,(screen.get_height() / 2) - 10,200,20), 0)
  pygame.draw.rect(screen, (255,255,255),((screen.get_width() / 2) - 102,(screen.get_height() / 2) - 12,204,24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  pygame.display.flip()
def ask(question):
    "ask(screen, question) -> answer"
    pygame.font.init()
    current_string = ''
    display_box(screen, question + ": " + str(current_string+""))
    while 1:
      inkey = get_key()
      if inkey == K_BACKSPACE:
        current_string = current_string[0:-1]
      elif inkey == K_RETURN:
        break
      elif inkey == K_MINUS:
        current_string.append("_")
      elif inkey <= 127:
        current_string+=(chr(inkey))
      display_box(screen, question + ": " + str(current_string+""))
    return str(current_string + "")

score = 0
#screen = pygame.display.set_mode((320,240))
name = ask("Name")
age = ask("Age")
while not game_over:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            save_data()
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]
            if event.key == pygame.K_LEFT:
                x -= shift_size
            elif event.key == pygame.K_RIGHT:
                x +=  shift_size
            elif event.key == pygame.K_DOWN:
                y +=  shift_size
            elif event.key == pygame.K_UP:
                y -=  shift_size
            x=max(x,0)
            x=min(x,WIDTH-player_size)
            y=max(y,0)
            y=min(y,HEIGHT-player_size)
            player_pos = [ x , y ]

    # clear screen again and again
    screen.fill(BLACK)

    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list,score)
    speed = (score//40)+10
    Level = speed-9

    time_now = round(time.time()-start_time,2)
    text1 = "Score: "+ str(score)
    text2 = "Level: "+ str(Level)
    text3 = "Timer: "+ str(time_now)



    if score>=Threshold :
        label1 = myFont.render(text1, 1, GREEN)
        text4 = "Threshold Passed"
        label4 = myFont.render(text4,1,GREEN)

    else:
        label1 = myFont.render(text1, 1, RED)
        text4 = "Threshold Not Passed"
        label4 = myFont.render(text4, 1, RED)


    label2 = myFont.render(text2, 1, YELLOW)
    label3 = myFont.render(text3, 1, YELLOW)
    screen.blit(label1,(WIDTH-220,HEIGHT-80))
    screen.blit(label4,(WIDTH/2,HEIGHT-40))
    screen.blit(label2,(10,HEIGHT-40))
    screen.blit(label3,(5,5))

    if collision_check(enemy_list,player_pos):
        game_over=True

        break;

    draw_enemies(enemy_list)

    pygame.draw.rect(screen, RED ,(player_pos[0] , player_pos[1] , player_size , player_size))

    # speed of for loop
    clock.tick(clock_time)

    # update the display
    pygame.display.update()

if game_over == True:
    save_data()
    pygame.quit()
