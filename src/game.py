#!/usr/bin/python2.7

import pygame, sys, os
from pygame.locals import *
from levelEditor import TextBox

pygame.init();

CWD = os.getcwd() + "/"
CWDI = CWD + "Images/"
CWDS = CWD + "/Sounds/"

DOWN = 0
LEFT = 1
UP = 2
RIGHT = 3

WIDTH = 800
HEIGHT = 600

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)

SWORD = 'sword'
ELECTRICITY = 'electricity'

IMAGESDICT = {'end block': pygame.image.load(CWDI + 'End_Block.png'),
              'corner block': pygame.image.load(CWDI + 'Corner.png'),
              'inside floor': pygame.image.load(CWDI + 'Plain_Block.png'),
              'grass': pygame.image.load(CWDI + 'Grass_Block.png'),
              'koder': pygame.image.load(CWDI + 'Koder.png'),
              'rock': pygame.image.load(CWDI + 'Rock.png'),
              'short tree': pygame.image.load(CWDI + 'Tree_Short.png'),
              'bush': pygame.image.load(CWDI + 'Tree_Bush.png'),
              'wall': pygame.image.load(CWDI + 'Wall.png'),
              'KODER': pygame.image.load(CWDI + 'koder1.png'),
              'KODERATTACK': pygame.image.load(CWDI + 'koder2.png'),
              'FEMALE1': pygame.image.load(CWDI + 'female1.png'),
              'MENUBG': pygame.image.load(CWDI + 'MenuBG.png'),
              'OKMENU': pygame.image.load(CWDI + 'OK.png'),
              'EXITMENU': pygame.image.load(CWDI + 'EXIT.png')}

SOUNDSDICT = {'mc 1': pygame.mixer.Sound(CWDS + 'mc_1.ogg'),
              'sword attack': pygame.mixer.Sound(CWDS + 'MC_sword1.ogg')}

IMAGESDICT['grass'] = pygame.transform.smoothscale(IMAGESDICT['grass'], (50, 85))  

MC_1 = pygame.mixer.Sound(CWDS + 'mc_1.ogg')

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.boardHeight = 10
        self.boardWidth = 10
        self.pos = [0, 0]
        self.pos[0], self.pos[1] = self.x * 50, self.y * 50
        self.animator = Animator("KODER")
        self.animator.addAttack("KODERATTACK", 70)
        self.movingSpeed = 2
        self.movingCurrent = 0
        self.animationSpeed = 3
        self.animationCurrent = 0
        self.moving = False
        self.attacking = None
        self.DIRECTION = DOWN
        self.DIRQUE = 1
        self.stopMoving = False
        self.worldObstacles = None
        self.weaponObject = None
        self.weaponX = 0
        self.weaponY = 0
        self.MIXER = pygame.mixer.Channel(2)
    def moveRight(self):
        if self.x + 1 < self.boardWidth - 1 and not self.moving and [self.x + 1, self.y] not in self.worldObstacles:
            self.moving = True
            self.attacking = None
            self.animator.imageNum = 0
            self.DIRECTION = RIGHT
            self.DIRQUE = RIGHT
        elif self.x + 1 < self.boardWidth - 1 and self.moving:
            self.DIRQUE = RIGHT
    def moveLeft(self):
        if self.x - 1 >= 0 and not self.moving and [self.x - 1, self.y] not in self.worldObstacles:
            self.moving = True
            self.attacking = None
            self.animator.imageNum = 0
            self.DIRECTION = LEFT
            self.DIRQUE = LEFT
        elif self.x - 1 >= 0 and self.moving:
            self.DIRQUE = LEFT
    def moveUp(self):
        if self.y - 1 >= 0 and not self.moving and [self.x, self.y - 1] not in self.worldObstacles:
            self.moving = True
            self.attacking = None
            self.animator.imageNum = 0
            self.DIRECTION = UP
            self.DIRQUE = UP
        elif self.y - 1 >= 0 and self.moving:
            self.DIRQUE = UP
    def moveDown(self):
        if self.y + 1 < self.boardHeight and not self.moving and [self.x, self.y + 1] not in self.worldObstacles:
            self.moving = True
            self.attacking = None
            self.animator.imageNum = 0
            self.DIRECTION = DOWN
            self.DIRQUE = DOWN
        elif self.y + 1 < self.boardHeight:
            self.DIRQUE = DOWN
    def moveDown2(self):
        if self.moving and self.DIRECTION == DOWN: self.stopMoving = True
    def moveUp2(self):
        if self.moving and self.DIRECTION == UP: self.stopMoving = True
    def moveRight2(self):
        if self.moving and self.DIRECTION == RIGHT: self.stopMoving = True
    def moveLeft2(self):
        if self.moving and self.DIRECTION == LEFT: self.stopMoving = True
    def attack(self, attack):
        self.attacking = attack
        if self.attacking == SWORD:
            self.MIXER.play(SOUNDSDICT['sword attack'])
        self.animator.imageNum = 0
        self.stopMoving = True
    def update(self):
        self.animationCurrent += 1
        self.movingCurrent += 1
        if self.movingCurrent == self.movingSpeed:
            if self.moving:
                self.updatePos(self.DIRECTION)
            self.movingCurrent = 0
        if self.animationCurrent == self.animationSpeed:
            self.animator.update(self.DIRECTION, self.moving, self.attacking)
            self.animationCurrent = 0
            if self.animator.stopAttacking:
                self.attacking = None
    def testProximity(self, obj):
        if (self.x - 1 == obj.x and obj.y == self.y or
	           self.x - 1 == obj.x and self.y - 1 == obj.y or
	           self.x - 1 == obj.x and self.y + 1 == obj.y or
	           self.x == obj.x and self.y + 1 == obj.y or
	           self.x == obj.x and self.y - 1 == obj.y or
	           self.x + 1 == obj.x and self.y - 1 == obj.y or
               self.x + 1 == obj.x and self.y + 1 == obj.y or
               self.x + 1 == obj.x and self.y == obj.y):
            return True
    def updatePos(self, DIR):
        if DIR == DOWN:
            self.pos[1] += 10 #make coords for drawing applicable
        elif DIR == UP:
            self.pos[1] -= 10 #make coords for drawing applicable
        elif DIR == RIGHT:
            self.pos[0] += 10 #make coords for drawing applicable
        elif DIR == LEFT:
            self.pos[0] -= 10 #make coords for drawing applicable
        
        if self.pos[0] % 50 == 0 and self.pos[1] % 50 == 0:
            self.x = self.pos[0] / 50
            self.y = self.pos[1] / 50
            self.moving = False
            if self.stopMoving:
                self.stopMoving = False
                self.moving = False
            elif self.DIRQUE != self.DIRECTION:
                if self.DIRQUE == DOWN: self.moveDown()
                elif self.DIRQUE == UP: self.moveUp()
                elif self.DIRQUE == RIGHT: self.moveRight()
                elif self.DIRQUE == LEFT: self.moveLeft()
            else:
                if self.DIRECTION == DOWN and (self.y + 1 == self.boardHeight or [self.x, self.y + 1] in self.worldObstacles): 
                    self.moving = False
                elif self.DIRECTION == UP and (self.y - 1 < 0 or [self.x, self.y - 1] in self.worldObstacles): 
                    self.moving = False
                elif self.DIRECTION == RIGHT and (self.x + 1 == self.boardWidth - 1 or [self.x + 1, self.y] in self.worldObstacles): 
                    self.moving = False
                elif self.DIRECTION == LEFT and (self.x - 1 < 0 or [self.x - 1, self.y] in self.worldObstacles): 
                    self.moving = False
                else: self.moving = True
    def setWorldSize(self, width, height):
        self.boardHeight = height
        self.boardWidth = width
    def setObstacles(self, obstacles):
        self.worldObstacles = obstacles
             
class World:
    def __init__(self, personName):
        self.player = None
        self.portalTo = 1
        self.people = []
        self.levelMap = []
        self.obstacles = []
        self.outPortals = {}
        self.portalsIn = {}
        self.level = 1
        self.loadPerson(personName)
        self.loadLevel(self.level)
        print self.portalsIn
        self.getObstacles()
        self.player.setObstacles(self.obstacles)
        self.player.setWorldSize(len(self.levelMap[0]), len(self.levelMap))
        self.MIXER = pygame.mixer.Channel(1)
        self.MIXER.play(SOUNDSDICT['mc 1'], -1)
    def update(self):
        self.player.update()
        for person in self.people:
            person.update()
        playerStrPos = str([int(self.player.x), int(self.player.y)])
        if playerStrPos in self.outPortals.keys():
            self.loadLevel(eval(self.outPortals[playerStrPos])[0], eval(self.outPortals[playerStrPos])[1])
            self.player.setWorldSize(len(self.levelMap[0]), len(self.levelMap))
            self.player.setObstacles(self.obstacles)
            return True
        return False
    def addPerson(self, person):
        self.people.append(person)
    def loadPerson(self, player):
        try:
            print CWD + "People/people.txt"
            file = open(CWD + "People/people.txt")
            file2 = open(CWD + "People/people.txt")
            fileData = file2.read()
            print player
            if player not in fileData:
                print("Player file is corrupt")
            else: #player exists in file
                while True:
                    line = file.readline()
                    if ";" in line:
                        print "';' in line"
                        continue
                    elif "#" in line:
                        if player in line:
                            self.level = int(file.readline())
                            personInfo = eval(file.readline())
                            print personInfo
                            self.player = Player(personInfo[0], personInfo[1])
                            playerAssets = eval(file.readline())
                            break
        except:
            print("Player file is missing")
    def loadLevel(self, level, portal=None):
        self.levelMap = []
        self.obstacles = []
        try:
            file = open(CWD + "Levels/level%s.txt" % level) #self.level)
        except:
            print("Level file doesn't exist")
            pygame.quit()
            sys.exit()
        file2 = open(CWD + "levels.txt")
        testString = file2.read()
        if "#1" in testString: #check to make sure file does contain levels and isn't just a random file.
            numOfLines = 0 #define a variable to store the length of the level
            while True: #create loop to find the correct level
                line = file.readline() #read the next line
                if ";" in line: #line is a comment
                    continue #move on to read the next line
                elif "#" in line: #line defines a level beginning
                    if str(1) in line: #if the level definition is the level wanted
                        numOfLines = int(file.readline()) #get the length of the level
                        break #start reading the level
                else: #line is a part of a level or is blank
                    continue #move on to read the next line
            for x in range (0, numOfLines):
                currentRow = []
                line = file.readline()
                for letter in line:
                    currentRow.append(letter)
                self.levelMap.append(currentRow)
            amountOfPeople = file.readline()
            for x in range(int(amountOfPeople)):
                personInfo = eval(file.readline())
                animator = Animator(personInfo[0])
                self.people.append(Person(animator, personInfo[1], personInfo[2], personInfo[3]))
            self.portalsIn = eval(file.readline())
            self.outPortals = eval(file.readline())
            if portal != None:
                self.player.x, self.player.y = self.portalsIn[portal][0], self.portalsIn[portal][1]
        else:
            print("Level file is corrupt")
            file.close()
            pygame.quit()
            sys.exit()
    def getObstacles(self):
        for y in range(len(self.levelMap)):
            for x in range(len(self.levelMap[y])):
                if self.levelMap[y][x] == "r":
                    self.obstacles.append([x, y])

class Renderer():
    def __init__(self, world):
        self.world = world #define world within this class
        self.levelSurface = pygame.Surface((len(self.world.levelMap[0]) *50, len(self.world.levelMap[0])*50))
        self.drawMap()
        self.SURFACE = pygame.Surface((self.levelSurface.get_width(), self.levelSurface.get_height()))
    def draw(self, cam):
        self.SURFACE.blit(self.levelSurface, (0, 0))
        self.SURFACE.blit(self.world.player.animator.currentImage, (self.world.player.pos[0] + self.world.player.animator.offsetX, self.world.player.pos[1] + self.world.player.animator.offsetY))
        for person in self.world.people:
            self.SURFACE.blit(person.animator.currentImage, (person.POS[0], person.POS[1]))
    def drawMap(self):
        self.levelSurface = pygame.Surface((len(self.world.levelMap[0]) *50, len(self.world.levelMap[0])*50))
        self.SURFACE = pygame.Surface((self.levelSurface.get_width(), self.levelSurface.get_height()))
        levelMap = self.world.levelMap
        for x in range (0, len(levelMap)):
            for y in range (0, len(levelMap[x])):
                if levelMap[x][y] == 'g':
                    self.levelSurface.blit(IMAGESDICT['grass'], (y*50, x*50))
                elif levelMap[x][y] == 'r':
                    self.levelSurface.blit(IMAGESDICT['grass'], (y *50, x*50))
                    self.levelSurface.blit(IMAGESDICT['rock'], (y *50, x*50))
                elif levelMap[x][y] == 'w':
                    self.levelSurface.blit(IMAGESDICT['grass'], (y *50, x*50))
                    self.levelSurface.blit(IMAGESDICT['wall'], (y *50, x*50))
                    
class Camera:
    def __init__(self, width, height, x, y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.movingUp = False
        self.movingDown = False
        self.movingRight = False
        self.movingLeft = False
    def up(self):
        self.movingUp = not self.movingUp
    def down(self):
        self.movingDown = not self.movingDown
    def right(self):
        self.movingRight = not self.movingRight
    def left(self):
        self.movingLeft = not self.movingLeft
    def setPos(self, x, y):
        self.x = x + self.width/2
        self.y = y + self.height/2
    def getX(self):
        return self.x - self.width/2
    def getY(self):
        return self.y - self.height/2
    def getPos(self):
        return (self.x, self.y)
    def update(self):
        if self.movingDown:
            self.y += 5
        if self.movingRight:
            self.x += 5
        if self.movingUp:
            self.y -= 5
        if self.movingLeft:
            self.x -= 5

class Animator:
    def __init__(self, FILE):
        self.totalImage = IMAGESDICT[FILE]
        self.images = []
        self.attackImages = []
        self.imageNum = 0
        self.amountOfAnimations = 4
        self.amountOfAnimations = self.totalImage.get_width()/50
        self.amountOfAttackAnimations = 0
        self.stopAttacking = False
        
        if self.totalImage.get_width() % 50 != 0:
            self.amountOfAnimations = 5
            self.totalImage = pygame.transform.scale(self.totalImage, (250, 200))
        yRange = self.totalImage.get_height()/50
        xRange = self.totalImage.get_width()/50
        self.offsetX = 0
        self.offsetY = 0
        for y in range(yRange):
            for x in range(xRange):
                img = pygame.Surface((50, 50), pygame.SRCALPHA)
                img.blit(self.totalImage, (0, 0), (50*x, 50*y, 50, 50))
                img = pygame.transform.scale(img, (50, 50))
                self.images.append(img)
        self.currentImage = self.images[0]
    def update(self, DIR, walking, attacking=None):
        self.stopAttacking = False
        if attacking == None:
            self.offsetX, self.offsetY = 0, 0
            if DIR == DOWN: base = 0;
            elif DIR == LEFT: base = self.amountOfAnimations;
            elif DIR == RIGHT: base = self.amountOfAnimations * 2;
            elif DIR == UP: base = self.amountOfAnimations * 3;
            else: base = 0
        else:
            if DIR == DOWN: 
                base = 0;
                self.offsetX, self.offsetY = 0, 0
            elif DIR == LEFT: 
                base = self.amountOfAttackAnimations;
                self.offsetX, self.offsetY = -10, 0
            elif DIR == RIGHT: 
                base = self.amountOfAttackAnimations * 2
                self.offsetX, self.offsetY = 0, 0
            elif DIR == UP: 
                base = self.amountOfAttackAnimations * 3;
                self.offsetX, self.offsetY = -5, 0
            else: base = 0;
        
        if attacking != None:
            if attacking == SWORD:
                self.imageNum += 1
                if self.imageNum == self.amountOfAttackAnimations - 1: 
                    self.imageNum = 1
                    self.stopAttacking = True
                self.currentImage = self.attackImages[base + self.imageNum]
        elif not walking:
            self.currentImage = self.images[base]
            self.imageNum = 0
        else:
            self.imageNum += 1
            if self.imageNum == self.amountOfAnimations - 1: self.imageNum = 1;
            self.currentImage = self.images[base + self.imageNum]  
    def addAttack(self, NAME, SIZE):
        self.amountOfAttackAnimations += IMAGESDICT[NAME].get_width()/SIZE
        for y in range(IMAGESDICT[NAME].get_height()/SIZE):
            for x in range(IMAGESDICT[NAME].get_width()/SIZE):
                TEMPSURF = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
                TEMPSURF.blit(IMAGESDICT[NAME], (0, 0), (SIZE*x, SIZE*y, SIZE, SIZE))
                self.attackImages.append(TEMPSURF)
        
class Person:
    def __init__(self, animator, pos, sayings = ["..."], path=[]):
        self.animator = animator
        self.direction = DOWN
        self.isWalking = False
        self.sayings = sayings
        self.path = path
        self.spotOnPath = 0
        self.speed = 10 #the higher the number the slower the person
        self.currentAnimationPosition = 0
        self.pos = pos
        self.POS = [pos[0] * 50, pos[1] * 50]
        self.nextPos = pos
        self.changeX = 0
        self.changeY = 0
    def update(self):
        self.currentAnimationPosition += 1
        if self.currentAnimationPosition == self.speed:
            self.currentAnimationPosition = 0
            if self.isWalking:
                self.POS[0] += self.changeX
                self.POS[1] += self.changeY
                if self.POS[0] % 50 == 0 and self.POS[1] % 50 == 0:
                    self.pos = self.path[self.spotOnPath]
                    self.changeX = 0
                    self.changeY = 0
                    self.isWalking = False
            else:
                self.spotOnPath += 1
                if self.spotOnPath == len(self.path):
                    self.spotOnPath = 0
                if self.path[self.spotOnPath][0] > self.pos[0]:
                    self.changeX = 12.5
                    self.direction = RIGHT
                    self.isWalking = True
                elif self.path[self.spotOnPath][0] < self.pos[0]:
                    self.changeX = -12.5
                    self.direction = LEFT
                    self.isWalking = True
                elif self.path[self.spotOnPath][1] > self.pos[1]:
                    self.changeY = -12.5
                    self.direction = UP
                    self.isWalking = True
                elif self.path[self.spotOnPath][1] < self.pos[1]:
                    self.changeY = 12.5
                    self.direction = DOWN
                    self.isWalking = True 
            self.animator.update(self.direction, self.isWalking)

def main():
    global DISPLAYSURF, FPSCLOCK, FPS
    #define the screen
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA, pygame.RESIZABLE)
    
    #define the Clock
    FPSCLOCK = pygame.time.Clock()
    FPS = 60
    
    #define camera
    cam = Camera(WIDTH, HEIGHT, WIDTH/2, HEIGHT/2)
    
    setUpPeopleImages()
    
    
    #GET THE INFO FOR STARTING THE WORLD PROPERLY
    playerName = menu()
    
    world = World(playerName)
    worldRenderer = Renderer(world) 
    while True:
        cam.setPos(-world.player.pos[0], -world.player.pos[1])
        cam.update()
        
        worldRenderer.draw(cam)
        if world.update():
            worldRenderer.drawMap()
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(worldRenderer.SURFACE, cam.getPos())
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    world.player.moveUp()
                elif event.key == K_s:
                    world.player.moveDown()
                elif event.key == K_d:
                    world.player.moveRight()
                elif event.key == K_a:
                    world.player.moveLeft()
                elif event.key == K_SPACE:
                    world.player.attack(SWORD)
                elif event.key == K_c:
                    pygame.image.save(DISPLAYSURF, "screenshotInGame.png")
            elif event.type == KEYUP:
                if event.key == K_w:
                    world.player.moveUp2()
                elif event.key == K_a:
                    world.player.moveLeft2()
                elif event.key == K_d:
                    world.player.moveRight2()
                elif event.key == K_s:
                    world.player.moveDown2()
        FPSCLOCK.tick(FPS)
        pygame.display.update()

def setUpPeopleImages():
    allPeople = pygame.image.load(CWDI + "people.png")
    peopleOnImage = ['ASH', 'ZACK', 'WHITEHAIR', 'MAILMAN', 'MAILWOMAN', 
                     'FLORIST', 'SWIMMER', 'ATHLETE', 'NURSE', 'SHELBY', 
                     'DAD', 'MOM', 'MARY', 'BUGWOMAN', 'CATWOMAN', 
                     'MARY2', 'PURPLEHAIR', 'SENSEI', 'KADE', 'ALEX',
                     'PROFESSOR', 'JACK', 'CLAIRE', 'LINK', 'LINKPURPLE']
    for y in range(allPeople.get_height()/200):
        for x in range(allPeople.get_width()/200):
            surf = pygame.Surface((200, 200), pygame.SRCALPHA)
            surf.blit(allPeople, (0, 0), (200 * x, 200 * y, 200, 200))
            IMAGESDICT[peopleOnImage[x + y * allPeople.get_width()/200]] = surf
    
    IMAGESDICT['MENUBG'] = pygame.transform.scale(IMAGESDICT['MENUBG'], (600, 600))
    

def menu():
    STARTWITH = 1
    RESUME = 2
    
    MENUSURF = pygame.Surface((WIDTH, HEIGHT))
    OKSURF   = pygame.Surface((100, HEIGHT))
    EXITSURF = pygame.Surface((100, HEIGHT))
    
    optWidth, optHeight = 400, 50
    optSelected = 0
    
    MENUOPTIONS = ["new file", "resume", "copyright kopperkow 2014"]
    MENUOPTIONSBOOL = [False, False]
    
    CURRENTOPTIONS = MENUOPTIONS
    CURRENTOPTIONSBOOL = MENUOPTIONSBOOL
    
    THISFONT = pygame.font.SysFont("Arial", 30, True, False)
    
    PLAYEROPTIONS = []
    foo = open(CWD + "People/people.txt", 'r')
    foo2 = open(CWD + "People/people.txt", 'r')
    readLength = foo2.read().count("#")
    readCount = 0
    while True:
        line = foo.readline()
        if '#' in line:
            readCount += 1
            PLAYEROPTIONS.append(line[1:].strip("\n"))
        if readCount == readLength: break
    PLAYEROPTIONSBOOL = [False for item in PLAYEROPTIONS]
    
    startingHeight = HEIGHT/3 + HEIGHT/3 - optHeight/2
    def updateMenuSurf():
        MENUSURF.fill(WHITE)
        MENUSURF.blit(IMAGESDICT['MENUBG'], (100, 0))
        MENUSURF.blit(OKSURF, (WIDTH - OKSURF.get_width(), 0))
        MENUSURF.blit(EXITSURF, (0, 0))
        
        for i in range(len(CURRENTOPTIONS)):
            TEXT = THISFONT.render(CURRENTOPTIONS[i].upper(), 1, BLACK)
            MENUSURF.blit(TEXT, (WIDTH/2 - TEXT.get_width()/2, startingHeight + i * 50 + 25 - TEXT.get_height()/2))
        for i in range(len(CURRENTOPTIONSBOOL)):
            if CURRENTOPTIONSBOOL[i]:
                pygame.draw.rect(MENUSURF, BLUE, (WIDTH/2 - optWidth/2, startingHeight + i * 50, optWidth, optHeight), 4)
                
    def updateOptions(optSelected):
        if optSelected in MENUOPTIONS:
            if optSelected == "new file":
                name = getName()
                foo = open(CWD + "People/people.txt", 'a')
                foo.write("\n")
                foo.write("#%s" % (name) + "\n")
                foo.write("1" + "\n")
                foo.write("[2, 2]" + "\n")
                foo.write("[]" + "\n")
                foo.close()
                return RESUME, MENUOPTIONS, MENUOPTIONSBOOL
            elif optSelected == "resume":
                return RESUME, PLAYEROPTIONS, PLAYEROPTIONSBOOL
        elif optSelected in PLAYEROPTIONS:
            return STARTWITH, PLAYEROPTIONS, PLAYEROPTIONSBOOL
            
    def getName():
        POPUPTEXT = TextBox(WIDTH/2, HEIGHT/2 - 50/2, optWidth, 50)
        while True:
            FPSCLOCK.tick(FPS)
            pygame.display.update()
            
            DISPLAYSURF.blit(MENUSURF, (0, 0))
            DISPLAYSURF.blit(POPUPTEXT.surface, (POPUPTEXT.x, POPUPTEXT.y))
            
            POPUPTEXT.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_RETURN and len(POPUPTEXT.getText()) >= 4:
                    return POPUPTEXT.getText()
                else:
                    POPUPTEXT.updateText(event)
    
    def drawBeginningSurfs():
        OKSURF.blit(IMAGESDICT['OKMENU'], (0, 0))
        EXITSURF.blit(IMAGESDICT['EXITMENU'], (0,0))
        OKTEXT = THISFONT.render("OK", 1, BLACK)
        EXITTEXT = THISFONT.render("EXIT", 1, BLACK)
        OKSURF.blit(OKTEXT, (OKSURF.get_width()/2 - OKTEXT.get_width()/2, OKSURF.get_height()/2 - OKTEXT.get_height()/2))
        EXITSURF.blit(EXITTEXT, (EXITSURF.get_width()/2 - EXITTEXT.get_width()/2, EXITSURF.get_height()/2 - EXITTEXT.get_height()/2))
    
    drawBeginningSurfs()
    
    while True:
        FPSCLOCK.tick(FPS)
        pygame.display.update()
        updateMenuSurf()
        
        DISPLAYSURF.blit(MENUSURF, (0,0))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    optSelected += 1
                    if optSelected == len(CURRENTOPTIONSBOOL):
                        optSelected = 0
                    for option in MENUOPTIONSBOOL: option = False
                    CURRENTOPTIONSBOOL[optSelected] = True
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                eventX, eventY = event.pos
                for i in range(len(CURRENTOPTIONSBOOL)):
                    if eventX >= WIDTH/2 - optWidth/2 and eventX <= WIDTH/2 + optWidth/2:
                        if eventY >= startingHeight + i * 50 and eventY <= startingHeight + i * 50 + 50:
                            CURRENTOPTIONSBOOL[i] = True
                        else:
                            CURRENTOPTIONSBOOL[i] = False
                    elif eventX <= EXITSURF.get_width():
                        pygame.quit()
                        sys.exit()
                    elif eventX >= WIDTH - OKSURF.get_width():
                        for i in range(len(CURRENTOPTIONSBOOL)):
                            if CURRENTOPTIONSBOOL[i]:
                                doNext, CURRENTOPTIONS, CURRENTOPTIONSBOOL = updateOptions(CURRENTOPTIONS[i])
                                if doNext == STARTWITH:
                                    return CURRENTOPTIONS[i]
                                elif doNext == RESUME:
                                    continue
    return
    
if __name__ == "__main__":
    pygame.init()
    main()