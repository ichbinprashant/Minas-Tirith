import pygame
import time
import random
import io

pygame.init()
pygame.mixer.init(frequency = 44100, size = -16, channels = 1,buffer = 2**12)
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)

display_width = 1000
display_height = 700
highscore_var = 0

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,51)
violet = (76,0,153)
grey = (64,64,64)
dark_white = (200,200,200)
dark_red = (200,0,0)
light_grey = (192,192,192)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('The Snake Game')
clock = pygame.time.Clock()

#mainmusic = pygame.mixer.music.load("music.wav")


largeText = pygame.font.SysFont('segoeprint',70)
smallText = pygame.font.SysFont('segoeprint',20)
mediumText = pygame.font.SysFont('aharoni', 35)
smallestText = pygame.font.SysFont('calibri', 15)
textinwhite = pygame.font.SysFont('cambria',20)

snake_headL = pygame.image.load('head.png')
snake_headR = pygame.transform.flip(snake_headL,True, False)
snake_headU = pygame.transform.rotate(snake_headL,-90)
snake_headD = pygame.transform.flip(snake_headU,False, True)
snake_head = snake_headR
snake_logo = pygame.transform.scale(snake_headR, (55, 34))
gameintro_snake = pygame.image.load('thesnake.png')

apple = pygame.image.load('apple.png')
icon = pygame.image.load('lolo.png')

body = pygame.image.load('bodyH.png')

background = pygame.image.load('background.png')
border = pygame.image.load('border.png')

pause = pygame.image.load('pause.png')
sound = pygame.image.load('sound.png')
close = pygame.image.load('close.png')
nosound = pygame.image.load('nosound.png')

arrowR = pygame.image.load('arrow.png')
arrowU = pygame.transform.rotate(arrowR,-90)
arrowL = pygame.transform.flip(arrowR,True, False)
arrowD = pygame.transform.rotate(arrowR,90)

pygame.display.set_icon(icon)    
x = 300
y = 354
score = 0

check = [1,0]
checker = 0
n = 0
m = 0
is_soundon = True
paused = True
apple_eaten = False
isit = True

def quit_game():
    pygame.quit()
    quit()
def text_object(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
def apple_generator():
    global m
    global n

    gameDisplay.blit(apple,(m,n))
    
def snake_display( snake_list):
    for abc in snake_list:
        gameDisplay.blit(body, (abc[0], abc[1] ))

def button(msg, x,y,w,h, inact,act, action = None):
        mouse1 = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse1[0] >x and y+h > mouse1[1] > y:
            pygame.draw.rect(gameDisplay, act, (x, y, w, h))
            if click[0] ==1 and action != None:
                action()
                
        else:
            pygame.draw.rect(gameDisplay, inact, (x, y, w, h))

        textSurf, textRect = text_object(msg, smallestText,black)
        textRect.center = ( (x+(w/2)), y+(h/2))
        gameDisplay.blit(textSurf, textRect)

def photo_button(photo,x,y,name, action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        

        if x+30 > mouse[0] >x and y+30 > mouse[1] > y:
            gameDisplay.blit(pygame.transform.scale(photo, (32, 32)), (x+1,y+1))
            

            
            textSurf, textRect = text_object(name, smallestText, red)
            textRect.center = ( (x+30), (y-10))
            gameDisplay.blit(textSurf, textRect)
            if click[0] ==1 and action != None:
                action()
                
        else:
            pygame.draw.rect(gameDisplay, black, (x-4,y-4,38,38))
            gameDisplay.blit(photo, (x,y))


def soundOnOff():
    global sound
    global nosound
    global checker
    global is_soundon
    temp = sound
    sound = nosound
    nosound = temp
    
    if checker%2 == 0:
        channel1.pause()
        
    if checker%2 !=0:
        channel1.unpause()
    checker +=1   
    

def unpause():
    global paused
    global checker
  
    paused = False
    if checker%2 ==0:
        channel1.unpause()
        
def pauser():
    global paused
    channel1.pause()
    pygame.draw.rect(gameDisplay, black, (396,296,208,108))
    pygame.draw.rect(gameDisplay, grey, (400,300,200,100))
    textSurf, textRect = text_object("Game Paused", textinwhite, white)
    textRect.center = ( 500, 320)
    gameDisplay.blit(textSurf, textRect)

    while paused:
                 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Continue", 425,350,70,20, dark_white,white, unpause)
        button("Quit", 500,350,70,20, dark_red,red, quit_game)
        pygame.display.update()
        clock.tick(15)
    paused = True  
    
    
def functionality():
    photo_button(sound, 850,110,'Music', soundOnOff)
    photo_button(close, 900,110,'Quit', game_intro)
    photo_button(pause, 800,110,'Pause', pauser)
        
def score_board(score):
    global highscore_var
    with io.open("myFile.txt", encoding ="utf-8")as myFile:
        highscore = [int(x) for x in myFile.read().split()]
    highscore_var = highscore[0]
    if score >= highscore[0]:
        with io.open("myFile.txt", mode = "w", encoding = "utf-8") as myFile:
            obj=str(score).decode('utf8')
            myFile.write(obj)
    text = smallText.render('High Score: '+ str(highscore[0]), True, black)
    gameDisplay.blit(text,(50,70))
    
    text = smallText.render('Score: '+ str(score), True, black)
    gameDisplay.blit(text,(50,100))
    
def backG(score):

    pygame.draw.rect(gameDisplay, white, (50,150,900,500))
    gameDisplay.blit(border,(50,150))
    TextSurf, TextRect = text_object("A Snake Game", mediumText, violet)
    TextRect.center = ((500), (50))
    gameDisplay.blit(TextSurf, TextRect)
    
    score_board(score)
    
def forisit():
    global isit
    isit = False
def controls():
    global isit
    gameDisplay.blit(background, (0,0))
    pygame.draw.rect(gameDisplay, black, (346,246,338,308))
    pygame.draw.rect(gameDisplay, white, (350,250,330,300))
    gameDisplay.blit(arrowR, (425, 300))
    gameDisplay.blit(arrowL, (425, 340))
    gameDisplay.blit(arrowU, (425, 390))
    gameDisplay.blit(arrowD, (425, 445))
    textSurf, textRect = text_object("CONTROLS:", smallText, black)
    textRect.center = ( 500, 280)
    gameDisplay.blit(textSurf, textRect)
    textSurf, textRect = text_object("-     move right", smallestText, black)
    textRect.center = ( 550, 325)
    gameDisplay.blit(textSurf, textRect)
    textSurf, textRect = text_object("-      move left", smallestText, black)
    textRect.center = ( 550, 365)
    gameDisplay.blit(textSurf, textRect)
    textSurf, textRect = text_object("-     move down", smallestText, black)
    textRect.center = ( 550, 415)
    gameDisplay.blit(textSurf, textRect)
    textSurf, textRect = text_object("-     move up", smallestText, black)
    textRect.center = ( 550, 460)
    gameDisplay.blit(textSurf, textRect)
    isit = True
    while isit:
                 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("OK", 590,525,70,20, dark_white, white,forisit)
          
        pygame.display.update()
        clock.tick(15)
def rules():
    global isit
    gameDisplay.blit(background, (0,0))
    pygame.draw.rect(gameDisplay, black, (346,246,318,288))
    pygame.draw.rect(gameDisplay, white, (350,250,310,280))
   
    textSurf, textRect = text_object("Rules", smallText, red)
    textRect.center = ( 500, 280)
    gameDisplay.blit(textSurf, textRect)
    
    text = smallestText.render("1)   Eat      by moving the snake.", True, black)
    gameDisplay.blit(text,(370,320))
    text = smallestText.render("2)   The score increases by eating the apple.", True, black)
    gameDisplay.blit(text,(370,365))
    text = smallestText.render("3)   On hitting the Boundry, The snake will die.", True, black)
    gameDisplay.blit(text,(370,415))
    text = smallestText.render("4)   The snake dies if it hits it's own body.", True, black)
    gameDisplay.blit(text,(370,460))
    isit = True
    while isit:
                 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("OK", 520,500,70,20, dark_white, white,forisit)
          
        pygame.display.update()
        clock.tick(15)    
      
def game_intro():
    intro = True
    channel1.pause()
    channel2.play(pygame.mixer.Sound("intro.wav"), loops = -1)
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        gameDisplay.blit(background, (0,0))
        
        gameDisplay.blit(gameintro_snake,(500-100,50))

        #button(msg, x,y,w,h, inact,act, action = None)
        button("START", 400, 450, 200, 30, white,light_grey, game_loop)
        button("CONTROLS", 400,490,200,30, white, light_grey, controls)
        button("RULES", 400,530,200,30, white, light_grey, rules)
        button("QUIT", 400,570,200,30, white, light_grey, quit_game)
        pygame.display.update()
        clock.tick(15)
    
def Hit(msg):
    channel1.stop()
    global paused
    global sound
    global nosound
    global highscore
    pygame.draw.rect(gameDisplay, black, (396,246,208,258))
    pygame.draw.rect(gameDisplay, grey, (400,250,200,250))
    textSurf, textRect = text_object("You're Dead!!!", textinwhite, white)
    textRect.center = ( 500, 300)
    gameDisplay.blit(textSurf, textRect)
    textSurf, textRect = text_object(msg, smallestText, green)
    textRect.center = ( 500, 320)
    gameDisplay.blit(textSurf, textRect)
    text = smallestText.render('Your score : '+ str(score), True, yellow)
    gameDisplay.blit(text,(450,350))
    text = smallestText.render('High Score : '+ str(highscore_var), True, yellow)
    gameDisplay.blit(text,(450,370))
    
    while paused:
                 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("New Game", 425,420,70,20, dark_white, white,game_loop)
        button("Quit", 500,420,70,20, dark_red,red, game_intro)  
        pygame.display.update()
        clock.tick(15)
    paused = True
    
        
def game_loop():
    global apple_eaten
    global m
    global n
    global sound
    global nosound
    global x
    global y
    global check
    global score
 
    speed = 22
    speedX = 0
    speedY = 0
    x = 300
    y = 354
    level_up = 1
    snakeLength = 3
    
    sound = pygame.image.load('sound.png')
    nosound = pygame.image.load('nosound.png')

    score = 0
    m = random.randint(100, 800)
    n = random.randint(170, 650)
    sound = pygame.image.load('sound.png')
    channel2.stop()
    channel1.play(pygame.mixer.Sound("music.wav"), loops = -1)
    gameEXIT = True
    
    global snake_head
    snake_list =[]
    
    while gameEXIT == True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if speedX == 0:
                        speedX = -(speed)
                        speedY = 0
                        snake_head = snake_headL
                        
                        headW = 64
                        headH = 50
                        check = [0,0]
                        
                if event.key == pygame.K_RIGHT:
                    if speedX == 0:
                        speedX = speed
                        speedY = 0
                        snake_head = snake_headR
                        
                        headW = 64
                        headH = 50
                        check = [1,0]
                        
                if event.key == pygame.K_UP:
                    if speedY==0:
                        speedX = 0
                        speedY = -(speed)
                        snake_head = snake_headU
                        
                        headW = 50
                        headH = 64
                        check = [0,1]
                       
                    
                if event.key == pygame.K_DOWN:
                    if speedY==0:
                        speedX = 0
                        speedY = speed
                        snake_head = snake_headD
                        
                        headW = 50
                        headH = 64
                        check = [1,1] 
                    
            if event.type == pygame.KEYUP:
                pass
        x += speedX
        y += speedY
        gameDisplay.blit(background, (0,0))
        
        backG(score)
        
        apple_generator()

        
        current = []
        current.append(x)
        current.append(y)
        snake_list.append(current)
        if len(snake_list) > snakeLength:
            del snake_list[0]

        
        snake_display( snake_list)
        gameDisplay.blit(snake_head, (x,y))
        for eachSegment in snake_list[2:-1]:
            if eachSegment == current:
                Hit("You hit yourself.")
        functionality()
        if level_up == 5 and speed<10:
             speed +=1
             level_up = 0


             
        if apple_eaten == True:
            m = round(random.randint(70 , 950-35))
            n = round(random.randint(170, 650-35))
            apple_eaten = False
            score += 1
            
            

        if  x < m+3 and x +22> m+3 and y < n+3 and y + 22> n+3:
            print("X crossover")
            apple_eaten=True
            level_up += 1
            snakeLength +=1
            
        if  x < m+17 and x +22> m+17 and y < n and y + 22> n:
            print("X crossover")
            apple_eaten=True
            level_up += 1
            snakeLength +=1
        if  x < m and x +22> m and y < n+17 and y + 22> n+17:
            print("X crossover")
            apple_eaten=True
            level_up += 1
            snakeLength +=1
        if  x < m+17 and x +22> m+17 and y < n+17 and y + 22> n+13:
            print("X crossover")
            apple_eaten=True
            level_up += 1
            snakeLength +=1

        if x < 50 + 21 or x> 950-20-20 or y < 170 or y + 22 > 700 - 80:
                Hit("You collided with the wall!")
                speedX =0
                speedY= 0
                print("LOL")

        
        pygame.display.update()
        clock.tick(15)


game_intro()     

pygame.quit()
quit()
