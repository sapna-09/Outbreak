import pygame
import random
import math 
from pygame import mixer

#initialisation
pygame.init() 

#creating screen
screen=pygame.display.set_mode((800,600))

#background image
background=pygame.image.load('fbg.png')

#background music
mixer.music.load('back.mp3')
mixer.music.play(-1)

#title and icon
pygame.display.set_caption("OUTBREAK")
icon = pygame.image.load('icon2.png')
pygame.display.set_icon(icon)

#players
playerImg = pygame.image.load('san.png')
playerX=370
playerY=480
playerX_change=0

#ENEMY
#insures that enemy appers at random position randint(start_pt, end_pt)
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num = 6

for i in range(num):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))     
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

#drop
#ready- we cant see the bulet on screen
#fire- drop is currently moving

dropImg = pygame.image.load('drop.png')
dropX=0      
dropY=480 
dropX_change=0
dropY_change=.4
drop_state="ready"

#score
score=0
font = pygame.font.Font('Blacklisted.ttf',32)
textX=10
textY=10

#game over text
over_font=pygame.font.Font('infected.ttf',80)

def show_score(x,y):
    score_val=font.render("Score: "+str(score),True,(0,0,120))
    screen.blit(score_val,(x,y))

def game_over():
    over_text= over_font.render("INFECTED Game Over",True,(51,0,0))
    screen.blit(over_text,(60,250))

def player(x,y):
    #drawing on screen using blit
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    #drawing on screen using blit
    screen.blit(enemyImg[i],(x,y))

def fire_drop(x,y):
    global drop_state
    drop_state="fire"
    #drop is fired from the top
    screen.blit(dropImg,(x+16,y+10))


def iscollision(enemyX,enemyY,dropX,dropY):
    distance = math.sqrt((math.pow(enemyX-dropX,2))+(math.pow(enemyY-dropY,2)))
    if distance<27:
        return True
    else:
        return False


#game loop
running=True
while running:
    #color of screen:red green blue
    screen.fill((0,0,100))
    #backgrond image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        #if key is prssed checked left or right
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-0.3
            if event.key==pygame.K_RIGHT:
                playerX_change=0.3
            if event.key==pygame.K_SPACE:
                if drop_state=="ready":
                    #sound
                    drop_sound=pygame.mixer.Sound('shoot.wav')
                    drop_sound.play()
                    dropX=playerX
                    fire_drop(dropX,dropY)
                    
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0

    #updating the value of x-coordinate
    playerX+=playerX_change
    
    #checking boundries so that spaceship doesnt go outside the display
    if playerX<=0:
        playerX=0
    elif playerX>=736:    #800-64px
        playerX=736       #it actually deletes the prev spaceship and create a new one 

    #enemy movement
    for i in range(num):
        #Game over
        if enemyY[i]>440:
            for j in range(num):
                enemyY[j]=2000
            game_over()
            break
        #updating the value of x-coordinate
        enemyX[i]+=enemyX_change[i]
        #checking boundries so that when enemy hits the end it moves in opposite direction
        if enemyX[i]<=0:
            enemyX_change[i]=0.2
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=736:    #800-64px
            enemyX_change[i]=-0.2
            enemyY[i]+=enemyY_change[i]

        #killing enemy and creating a new one
        collision= iscollision(enemyX[i],enemyY[i],dropX,dropY)
        if collision:
            collision_sound=pygame.mixer.Sound('explosion.wav')
            collision_sound.play()
            dropY=480
            drop_state="ready"
            #updating score with each kill
            score+=1
            #creating new enemy
            enemyX[i]=random.randint(0,735)      
            enemyY[i]=random.randint(50,150)
        enemy(enemyX[i],enemyY[i],i)

    #drop movement
    if dropY<=0:
        dropY=480
        drop_state="ready"
      
    if drop_state == "fire":
        fire_drop(dropX,dropY)
        dropY-=dropY_change

    #CALL THE PLAYER FUNCTION AFTER SCREEN FILL FUNCTION
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()
