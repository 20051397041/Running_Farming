
from random import randint
from re import S
from turtle import speed, update
import pygame
import sys

pygame.init()

# 3.1 - Load audio
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("rawr.wav")
hit_sound.set_volume(1)

# background music
pygame.mixer.music.load("ost.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

class Petani():
    def __init__(self):
        self.sprites = [image_load("duck.png",(90,90)),
                        image_load("Farmer2.png",(90,90)),
                        image_load("Farmer3.png",(90,90)),
                        image_load("Farmer4.png",(90,90))]
        
        self.rect = self.sprites[0].get_rect()
        self.rect.x = 10
        self.rect.width = 40
        self.currSprite = 0
        self.jump = 0
        self.onTheGround = False
        
    
    def update(self):
        self.onTheGround = False

        #jump
        self.rect.move_ip(0,self.jump)
        self.jump+=0.4

        #ground
        if(self.rect.bottom > 270):
            self.rect.bottom = 270
            self.onTheGround = True

    def jumpRex(self):
        if(self.onTheGround):
            self.jump = -13

    def draw(self): 
        global screen
        
        if(self.currSprite == 3):
            self.currSprite = 3
        elif(self.onTheGround ):
            if(self.currSprite <= 1 ):
                self.currSprite = 2
            else:
                self.currSprite = 1
        else:
            self.currSprite = 0
        
        screen.blit(self.sprites[self.currSprite],self.rect)
    
    def dead(self):
        self.currSprite = 3
    def isDead(self):
        return self.currSprite == 3

class Clouds():
    def __init__(self,path,x,y):
        self.sprite = image_load(path,(50,30))
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        global width
        self.rect.move_ip(-1.7,0)
        if(self.rect.right < 0):
            self.rect.left = width+30
            self.rect.y = randint(10,200)
    def draw(self):
        global screen
        screen.blit(self.sprite,self.rect)

class Cactus():
    def __init__(self,x):
        self.sprites = [image_load("musuh1.png",(40,50)),
                        image_load("musuh2.png",(60,60)),
                        image_load("musuh3.png",(65,65))]
        
        
        self.speed = -3.5
        self.currSprite = randint(0,2)
        self.rect = self.sprites[self.currSprite].get_rect()
        self.rect.x = x
        self.rect.bottom = 270
    def update(self):
        global width
        self.rect.move_ip(self.speed,0)

        if(Farmer.rect.colliderect(self.rect)):
            Farmer.dead()
        
        if(self.rect.right < 0):
            self.rect.left = width*4
            self.currSprite = randint(0,2)
            self.rect.size = self.sprites[self.currSprite].get_rect().size
            self.speed -= 0.1
    def draw(self):
        global screen
        screen.blit(self.sprites[self.currSprite],self.rect)

class Score():
    def __init__(self) -> None:
        self.score = 0
        self.sheet = image_load("score.png")

        self.Index = [
            pygame.Rect(0,0,20,25),
            pygame.Rect(18,0,20,25),
            pygame.Rect(18*2+2,0,20,25),
            pygame.Rect(18*3+4,0,20,25),
            pygame.Rect(18*4+6,0,20,25),
            pygame.Rect(18*5+8,0,20,25),
            pygame.Rect(18*6+11,0,20,25),
            pygame.Rect(18*7+12,0,20,25),
            pygame.Rect(18*8+14,0,20,25),
            pygame.Rect(18*9+16,0,20,25),
        ]
        
    def inc(self):
        self.score+=1
    def clear(self):
        self.score = 0
    def draw(self):
        global screen
        sc = int(self.score/10)
        arrIndex = list()

        while(sc!=00):
            arrIndex.insert(0,int(sc%10))
            sc = int(sc/10)
    
        for i in range(len(arrIndex)):
            screen.blit(self.sheet.subsurface(self.Index[arrIndex[i]]),pygame.Rect(600+i*24,0,20,25))



def image_load(path,size = None):
    new_surface = pygame.image.load(path)
    if size!=None :
        new_surface = pygame.transform.scale(new_surface,size)
    return new_surface

def setup():
    global clouds,cactus,tscore
    clouds = [Clouds("cloud.png",width,50),
        Clouds("cloud.png",width+100,150),
        Clouds("cloud.png",width+600,200),
        Clouds("cloud.png",width-400,70),
        Clouds("cloud.png",width-50,111)] 


    cactus = [Cactus(width),
          Cactus(width+600),
          Cactus(width+1100),
          Cactus(width+1600),
          Cactus(width+2300)]

    tscore.clear()

def update():
    global Farmer,clouds,cactus,tscore
    Farmer.update()
    
    for c in clouds:
        c.update()
    for c in cactus:
        c.update()
    
    tscore.inc()
    
def draw():
    global screen,Farmer,cactus,clouds,gameOver,buttonGameOver,tscore
    screen.fill((100,100,100))
    screen.fill((180,180,180),pygame.Rect(0,260,width,100))

    for c in clouds:
        c.draw()

    for c in cactus:
        c.draw()
    
    Farmer.draw()

    tscore.draw()

    if(Farmer.isDead()):
        goImg = gameOverImg.get_rect()
        goImg.center = (width/2,height/2)
        screen.blit(gameOverImg,goImg)
        goImg.center = (553,height/2+40)
        screen.blit(buttonGameOver,goImg)
        hit_sound.play()

    pygame.display.flip()

#global variabals 
winSize = width,height = 800,360
screen = pygame.display.set_mode(winSize,vsync=1)
Run = False
gameOverImg = image_load("gameover.png")
buttonGameOver = image_load("button.png")
hit_sound.play()

Farmer = Petani() 

clouds = None
cactus = None

tscore = Score()

setup()

while(not Run):

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_SPACE]:
            Farmer.jumpRex()
        
    if(Farmer.isDead()):
        pygame.event.clear()
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_r]:
            Farmer = Petani()
            setup()
    else:
        update()

    draw()

    pygame.time.Clock().tick(120)