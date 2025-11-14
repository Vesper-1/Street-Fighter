import pygame
import math
from pygame import mixer
import os
import random

pygame.init()

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH , HEIGHT))

pygame.display.set_caption("Space Fighter")
icon = pygame.image.load(os.path.join('assets', 'icon.png'))
pygame.display.set_icon(icon)

background = pygame.image.load(os.path.join('assets', 'bg.png'))

mixer.music.load(os.path.join('sounds', 'bgmusic.mp3'))
mixer.music.play(-1)

multiplayer = False

player1 = pygame.transform.scale(
    pygame.transform.flip(
        pygame.image.load(
            os.path.join('assets', 'player1.png')), True, False), (70,70))
player1X = 20
player1Y = HEIGHT/2 - 35
player1_change = 0

player2 = pygame.transform.scale(
    pygame.transform.flip(
        pygame.image.load(
            os.path.join('assets', 'player2.png')), False, False), (70,70))
player2X = WIDTH - 90
player2Y = HEIGHT/2 - 35
player2_change = 0

bullet1 = pygame.transform.scale(
    pygame.transform.rotate(
        pygame.image.load(os.path.join('assets', 'bullet.png')), 90), (60, 60))
bullet1X = 0
bullet1Y = 0
bullet1_change = 5
fire1 = True

bullet2 = pygame.transform.scale(
    pygame.transform.rotate(
        pygame.image.load(os.path.join('assets', 'bullet.png')), -90), (60, 60))
bullet2X = 0
bullet2Y = 0
bullet2_change = 5
fire2 = True

scoreOne = scoreTwo =0

font = pygame.font.Font(os.path.join('fonts', 'Gameplay.ttf'), 32)
over_font = pygame.font.Font(os.path.join('fonts', 'Gameplay.ttf'), 70)

text1X = 20
text1Y = 20
text2X = WIDTH - 230
text2Y = 20

def playerOneMovement(X, Y):
    screen.blit(player1, (X, Y + 15))

def playerTwoMovement(X, Y):
    screen.blit(player2, (X, Y + 15))

bot_up = 0
bot_down = 0

def botMovement():
    global bot_up, bot_down
    up_down = random.choice(["UP", "DOWN"])
    if up_down == "UP": 
        bot_up += random.randint(35, 70)
    else:
        bot_down += random.randint(35, 70)

def bullet1Movement(X, Y):
    global fire1
    fire1 = False
    screen.blit(bullet1, (X + 45, Y + 22))

def bullet2Movement(X, Y):
    global fire2
    fire2 = False
    screen.blit(bullet2, (X - 15, Y + 22))

def collisionDetectorPlayerOne(b1x, b1y, p2x , p2y):
    global fire1
    global bullet1X 
    global bullet1Y 
    if int(math.sqrt(math.pow(p2x - b1x, 2) + math.pow(p2y - b1y, 2))) < 60:
        fire1 = True
        bullet1X = 0
        bullet1Y = 0
        return True
def collisionDetectorPlayerTwo(b2x, b2y, p1x, p1y):
    global fire2
    global bullet2X 
    global bullet2Y 
    distance = int(math.sqrt(math.pow(b2x - p1x, 2) + math.pow(b2y - p1y, 2)))
    if distance < 60:
        fire2 = True
        bullet2X = 0
        bullet2Y = 0
        return True

def blit_text_center(text, win, color):
    render = font.render(text, 1, color)
    win.blit(render, (WIDTH // 2 - render.get_width() // 2, HEIGHT // 2 - render.get_height() // 2)) #render: change text to image

def blit_text(text, win, font_size, color, x, y):
    over_font = pygame.font.Font(os.path.join('fonts', 'Gameplay.ttf'), font_size-20)
    render = over_font.render(text, 1, color)
    win.blit(render, (x, y))

def displayScore(X, Y):
    score = font.render("Score : " + str(scoreOne), True, (255, 255, 255))
    screen.blit(score, (X, Y))

def displayScoreTwo(X, Y)   :
    score = font.render("Score : " + str(scoreTwo), True, (255, 255, 255))
    screen.blit(score, (X, Y))

def show_main_menu(win):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        if event.type == pygame.KEYDOWN:
              if event.key  == pygame.K_RETURN:
                    return False

    win.blit(background, (0, 0))
    blit_text_center("Press Enter key to begin!", win, (255, 255, 255))
    blit_text("Player 1 Controls", win, 40, (255, 255, 255), *(10, 10))
    blit_text("W - Move Up", win, 40, (255, 255, 255), *(10, 50))
    blit_text("S - Move Down", win, 40, (255, 255, 255), *(10, 90))
    blit_text("SPACE - Action key", win, 40, (255, 255, 255), *(10, 130))
    blit_text("Player 2 Controls", win, 40, (255, 255, 255), *(500, 10))
    blit_text("UP - Move Up", win, 40, (255, 255, 255), *(500, 50))
    blit_text("DOWN - Move Down", win, 40, (255, 255, 255), *(500, 90))
    blit_text("L-OPTION - Action key", win, 40, (255, 255, 255), *(500, 130))
    pygame.display.update()
    
    return True

def show_game_mode_menu(win):
    """
    It returns a tuple of two bool, the first index is the bool for the multiplayer while the second is the bool for the game mode menu
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key  == pygame.K_s:
                return False, False
            if event.key == pygame.K_m:
                return True, False


    win.blit(background, (0, 0))
    blit_text("Chose Your Game Mode", win, 50, (255, 255, 255), *(210, 230))
    blit_text("Press 'M' key for Multiplayer and 'S' key for Single Player", win, 40, (255, 255, 255), *(20, 270))
    pygame.display.update()
    return True,True

def gameover():
    global scoreOne
    global scoreTwo
    blit_text(f"GAMEOVER", screen, 60, (255, 255, 255), 270, 230)

    if scoreOne == 10:
        blit_text_center(f"PLAYER ONE WON", screen, (255, 255, 255))

    elif scoreTwo == 10:
        blit_text_center(f"PLAYER TWO WON", screen, (255, 255, 255))
    
    scoreOne = 0
    scoreTwo = 0

running = True
main_menu = True
game_mode = True
while running:
 
    screen.blit(background, (0, 0))
    if main_menu:
        main_menu = show_main_menu(screen)
        continue
    if game_mode:
        game_mode_menu = show_game_mode_menu(screen)
        multiplayer = game_mode_menu[0]
        game_mode = game_mode_menu[1]
        continue

    for event in pygame.event.get():
          if event.type == pygame.QUIT:
             running = False
          if event.type == pygame.KEYDOWN:
              if event.key  == pygame.K_w:
                  player1_change = -3
               
              if event.key == pygame.K_s:
                  player1_change = +3

              if event.key == pygame.K_SPACE:
                  if fire1 is True:
                    fire1_sound = mixer.Sound(os.path.join('sounds', 'fire1.wav'))
                    fire1_sound.play()
                    bullet1X = player1X
                    bullet1Y = player1Y
                    bullet1Movement(bullet1X, bullet1Y)
            
          if event.type == pygame.KEYUP:
              if event.key == pygame.K_w or event.key == pygame.K_s:
                 player1_change = 0
          if event.type == pygame.KEYDOWN:
            if multiplayer:
                if event.key  == pygame.K_UP:
                    player2_change = -3
                
                if event.key == pygame.K_DOWN:
                    player2_change = +3

                if event.key == pygame.K_RALT:
                    if fire2 is True:
                        fire2_sound = mixer.Sound(os.path.join('sounds', 'fire1.wav'))
                        fire2_sound.play()  
                        bullet2X = player2X
                        bullet2Y = player2Y
                        bullet2Movement(bullet2X, bullet2Y)
                   
          if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2_change = 0
    if not multiplayer:
        if bot_up > 0 and bot_down == 0:
            player2_change = -1
            bot_up -= 1
        elif bot_up <= 0 and bot_down == 0:
            botMovement()
        if bot_up % 2 == 0:
            if fire2 is True:
                fire2_sound = mixer.Sound(os.path.join('sounds', 'fire1.wav'))
                fire2_sound.play()  
                bullet2X = player2X
                bullet2Y = player2Y
                bullet2Movement(bullet2X, bullet2Y)
        
        if bot_down > 0 and bot_up == 0:
            player2_change = +1
            bot_down -= 1
        elif bot_down <= 0 and bot_up == 0:
            botMovement()
        
        if bot_down % 2 == 0:
            if fire2 is True:
                fire2_sound = mixer.Sound(os.path.join('sounds', 'fire1.wav'))
                fire2_sound.play()  
                bullet2X = player2X
                bullet2Y = player2Y
                bullet2Movement(bullet2X, bullet2Y)
    player1Y += player1_change 

    if player1Y <= 70:
        player1Y = 70
    
    if player1Y >= HEIGHT-90:
        player1Y = HEIGHT-90
    
    
    player2Y += player2_change 

    if player2Y <= 70:
        player2Y = 70
    
    if player2Y >= HEIGHT-90:
        player2Y = HEIGHT-90

    if bullet1X >= WIDTH :
        fire1 = True

    if fire1 is False:
        bullet1Movement(bullet1X, bullet1Y)    
        bullet1X += bullet1_change

    if bullet2X <= 0:
        fire2 = True

    if fire2 is False:
        bullet2Movement(bullet2X, bullet2Y)    
        bullet2X -= bullet2_change

    if collisionDetectorPlayerOne(bullet1X, bullet1Y, player2X, player2Y) is True:
       scoreOne += 1

    if collisionDetectorPlayerTwo(bullet2X, bullet2Y, player1X, player1Y) is True:
       scoreTwo += 1
    
    displayScore(text1X, text1Y)
    displayScoreTwo(text2X, text2Y)
    playerOneMovement(player1X, player1Y)
    playerTwoMovement(player2X, player2Y)
    if not multiplayer:
        pygame.display.update()

    if scoreOne == 10 or scoreTwo == 10:
        gameover()
        pygame.display.update()
        pygame.time.delay(6000)
        main_menu = game_mode = True
        bot_up = bot_down = 0
        player1Y = player2Y = HEIGHT/2 - 35
        playerOneMovement(player1X, player1Y)
        playerTwoMovement(player2X, player2Y)
    
    pygame.display.update()