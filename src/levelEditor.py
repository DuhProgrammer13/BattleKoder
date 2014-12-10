#!/usr/bin/python2.7

import pygame, os, sys
from pygame.locals import *

#define screen variables
SCREEN_W = 800
SCREEN_H = 600

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
T_BLUE = (30, 30, 255, 128)
T_RED = (255, 20, 20, 128)

BLOCKS = 'blocks'
PEOPLE = 'peeps'
TEXTBOX = 'text'
SAVE = 'save'

CURRENTACTION = None

CWDF = os.getcwd() + "/Levels/"
CWDI = os.getcwd() + "/Images/"

IMAGESDICT = {'corner block': pygame.image.load(CWDI + 'Corner.png'),
              'inside floor': pygame.image.load(CWDI + 'Plain_Block.png'),
              'grass': pygame.image.load(CWDI + 'Grass_Block.png'),
              'koder': pygame.image.load(CWDI + 'Koder.png'),
              'rock': pygame.image.load(CWDI + 'Rock.png'),
              'short tree': pygame.image.load(CWDI + 'Tree_Short.png'),
              'bush': pygame.image.load(CWDI + 'Tree_Bush.png'),
              'wall': pygame.image.load(CWDI + 'Wall.png'),
              'empty_block' : pygame.image.load(CWDI + "empty.png"),
              'KODER': pygame.image.load(CWDI + 'koder1.png'),
              'FEMALE1': pygame.image.load(CWDI + 'female1.png')}

PEOPLEDICT = [['KODER', 'k'],
              ['FEMALE1', 'f']]

PEOPLEDICT2= {b:a for a, b in PEOPLEDICT}

PEOPLEOPTIONS = [False for item in PEOPLEDICT]

BLOCKSDICT = [['corner block', 'c'],
              ['inside floor', 'i'],
              ['grass', 'g'],
              ['rock', 'r'],
              ['short tree', 't'],
              ['bush', 'b'],
              ['wall', 'w'],
              ['empty_block', 'e']]

BLOCKSDICT2 = {"c": "corner block",
               "i": "inside floor",
               "g": "grass",
               "r": "rock",
               "t": "short tree",
               "b": "bush",
               "w": "wall",
               "e": "empty_block"}

BLOCKOPTIONS = [False for item in BLOCKSDICT]

def setupPeople():
    for item in PEOPLEDICT:
        if item[1] == 'k':
            surf = pygame.Surface((50, 50), pygame.SRCALPHA)
            surf.blit(IMAGESDICT[item[0]], (0,0), (0,0,50,50))
        else:
            surf = pygame.Surface((25, 30), pygame.SRCALPHA)
        surf.blit(IMAGESDICT[item[0]], (0,0), (0,0,25, 30))
        surf = pygame.transform.scale(surf, (50, 50))
        IMAGESDICT[item[0]] = surf
def setupBlocks():
    IMAGESDICT["grass"] = pygame.transform.scale(IMAGESDICT["grass"], (50, 80))
    IMAGESDICT["inside floor"] = pygame.transform.scale(IMAGESDICT["inside floor"], (50, 80))
        
class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = []
        self.people = []
        self.person = DynamicPerson([2, 2])
        for i in range(width):
            self.map.append(["e" for item in range(height)])
        self.map[1][1] = "r"
        self.portalsIn = {}
        self.portalsOut = {}
        self.selectedPortal = None
    def addAbove(self):
        newAddition = ["e" for i in self.map[0]]
        self.map.append(newAddition)
        for i in range(len(self.map) - 1, 0, -1):
            self.map[i] = self.map[i-1]
        self.map[0] = newAddition
        self.person.updatePos(self.person.x, self.person.y + 1)
        self.height += 1
    def addBelow(self):
        newAddition = ["e" for item in self.map[0]]
        self.map.append(newAddition)
        self.height += 1
    def addRight(self):
        for item in self.map:
            item.append("e")
        self.width += 1
    def addLeft(self):
        for item in self.map:
            item.append("e")
            for i in range(len(item) - 1, 0, -1):
                item[i] = item[i-1]
            item[0] = "e"
        self.width += 1
        self.person.updatePos(self.person.x + 1, self.person.y)
    def addPerson(self, image, pos, name):
        self.people.append(Person(image, pos, name))

class Renderer:
    def __init__(self, world):
        self.world = world
        self.SURFACE = pygame.Surface((len(self.world.map) * 50 + 30, len(self.world.map[0]) * 50 + 30), pygame.SRCALPHA)
    def drawMap(self):
        self.refreshSurface()
        for y in range(len(self.world.map)):
            for x in range(len(self.world.map[y])):
                letter = self.world.map[y][x]
                if letter == "r":
                    self.SURFACE.blit(IMAGESDICT["grass"], (x * 50, y * 50))
                    self.SURFACE.blit(IMAGESDICT["rock"], (x * 50, y * 50))
                elif letter == "t":
                    self.SURFACE.blit(IMAGESDICT["grass"], (x * 50, y * 50))
                    self.SURFACE.blit(IMAGESDICT["short tree"], (x * 50, y * 50))
                elif letter == "b":
                    self.SURFACE.blit(IMAGESDICT["grass"], (x * 50, y * 50))
                    self.SURFACE.blit(IMAGESDICT["bush"], (x * 50, y * 50))
                elif letter == "w":
                    self.SURFACE.blit(IMAGESDICT["grass"], (x * 50, y * 50))
                    self.SURFACE.blit(IMAGESDICT["wall"], (x * 50, y * 50 - 30))
                else:
                    self.SURFACE.blit(IMAGESDICT[BLOCKSDICT2[letter]], (x * 50, y * 50))
                if self.world.person.pos[0] == x and self.world.person.pos[1] == y:
                    self.SURFACE.blit(IMAGESDICT["KODER"], (x * 50, y * 50))
        for person in self.world.people:
            self.SURFACE.blit(person.image, person.POS)
    def refreshSurface(self):
        self.SURFACE = pygame.Surface((len(self.world.map[0]) * 50, len(self.world.map) * 50 + 30), pygame.SRCALPHA)
        
class Camera:
    def __init__(self, width, height, x, y):
        self.x = x - width/2
        self.y = y - height/2
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
        self.x = x - self.width/2
        self.y = y - self.height/2
    def getX(self):
        return self.x
    def getY(self):
        return self.y
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
    def clickToCamera(self, x, y):
        return [x - self.x, y - self.y]
    def sudoScroll(self, down, up, top, bottom):
        if down and self.height - self.y != bottom and self.height - self.y <= bottom:
            self.y -= 10
        if up and self.y != top:
            self.y += 10

class LeftSidebar:
    def __init__(self):
        self.SELECTEDBLOCK = "w"
        self.SELECTEDPERSON = "KODER"
        self.SURFACE = pygame.Surface((80, SCREEN_H), pygame.SRCALPHA)
        self.BLOCKSURF  = pygame.Surface((50, SCREEN_H - 160), pygame.SRCALPHA)
        self.camera = Camera(50, SCREEN_H - 160, 0, 0)
        self.goingOut = False
        self.x = -80
        self.y = 0
        pygame.draw.polygon(self.SURFACE, T_BLUE, ((0, 0), (80, 80), (80, SCREEN_H - 80), (0, SCREEN_H)))
    def update(self):
        if self.goingOut and self.x < 0:
            self.x += 5
        elif not self.goingOut and self.x > -80:
            self.x -= 5
        self.draw()
    def draw(self):
        self.SURFACE = pygame.Surface((80, SCREEN_H), pygame.SRCALPHA)
        self.BLOCKSURF = pygame.Surface((50, SCREEN_H - 160), pygame.SRCALPHA)
        if CURRENTSCREEN == BLOCKS:
            for i in range(len(BLOCKSDICT)):
                self.BLOCKSURF.blit(IMAGESDICT[BLOCKSDICT[i][0]], (0, i*100 + self.camera.y))
                if BLOCKOPTIONS[i]:
                    pygame.draw.rect(self.BLOCKSURF, BLUE, (0, i * 100 + self.camera.y, IMAGESDICT[BLOCKSDICT[i][0]].get_width(), IMAGESDICT[BLOCKSDICT[i][0]].get_height()), 4)
        elif CURRENTSCREEN == PEOPLE:
            for i in range(len(PEOPLEDICT)):
                self.BLOCKSURF.blit(IMAGESDICT[PEOPLEDICT[i][0]], (0, i*100 + self.camera.y))
                if PEOPLEOPTIONS[i]:
                    pygame.draw.rect(self.BLOCKSURF, BLUE, (0, i*100 + self.camera.y, IMAGESDICT[PEOPLEDICT[i][0]].get_width(), IMAGESDICT[PEOPLEDICT[i][0]].get_height()), 4)
        pygame.draw.polygon(self.SURFACE, T_BLUE, ((0, 0), (80, 80), (80, SCREEN_H - 80), (0, SCREEN_H)))
        self.SURFACE.blit(self.BLOCKSURF, (15, 80))
    def scrollOut(self):
        self.goingOut = True
    def scrollIn(self):
        self.goingOut = False
    def updateEvent(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4:
                if CURRENTSCREEN == BLOCKS:
                    self.camera.sudoScroll(False, True, 0, len(BLOCKSDICT) * 100)
                else:
                    self.camera.sudoScroll(False, True, 0, len(PEOPLEDICT) * 100)
            elif event.button == 5:
                if CURRENTSCREEN == BLOCKS:
                    self.camera.sudoScroll(True, False, 0, len(BLOCKSDICT) * 100)
                else:
                    self.camera.sudoScroll(True, False, 0, len(PEOPLEDICT) * 100)
            elif event.button == 1:
                X = event.pos[0]
                Y = event.pos[1]
                X = X + self.x
                Y = Y - self.camera.getY() - 80
                #X, Y = self.camera.clickToCamera(X, Y)
                if X >= 15 and X <= 65:
                    if CURRENTSCREEN == BLOCKS:
                        for i in range(len(BLOCKSDICT)):
                            if Y >= i * 100 and Y <= i * 100 + 100:
                                BLOCKOPTIONS[i] = True
                                self.SELECTEDBLOCK = BLOCKSDICT[i][1]
                            else:
                                BLOCKOPTIONS[i] = False
                    elif CURRENTSCREEN == PEOPLE:
                        for i in range(len(PEOPLEDICT)):
                            if Y >= i * 100 and Y <= i * 100 + 100:
                                PEOPLEOPTIONS[i] = True
                                self.SELECTEDPERSON = PEOPLEDICT[i][0]
                            else:
                                PEOPLEOPTIONS[i] = False

class BottomBar:
    def __init__(self, x, y, width, height):
        self.options = [BLOCKS, PEOPLE, SAVE]
        self.optionsBool = [[item, False] for item in self.options]
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.SURFACE = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.font = pygame.font.SysFont("Arial", 16, True, False)
        self.goingOut = False
        self.update()
    def updateEvent(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                X, Y = event.pos
                if X <= self.x + 80 or X >= self.x +self.width - 80 or Y <= 15 + self.y or Y >= self.y + self.width - 15:
                    return
                for i in range(len(self.options)):
                    if X >= i * 100 + self.x + 80 and X <= i * 100 + 100 + self.x + 80:
                        self.optionsBool[i][1] = True
                    else:
                        self.optionsBool[i][1] = False
    def update(self):
        global CURRENTSCREEN
        if self.goingOut and self.y > SCREEN_H - 80:
            self.y -= 5
        elif not self.goingOut and self.y < SCREEN_H:
            self.y += 5
            
        for item in self.optionsBool:
            if item[1]:
                CURRENTSCREEN = item[0]
                
        self.draw()
    def scrollOut(self):
        self.goingOut = True
    def scrollIn(self):
        self.goingOut = False
    def draw(self):
        self.SURFACE = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.polygon(self.SURFACE, T_BLUE, ((0, 80), (80, 0), (self.width-80, 0), (self.width, 80)))
        for i in range(len(self.options)):
            pygame.draw.rect(self.SURFACE, RED, (i * 100 + 80 - 1, 16, 48, 48))
            text = self.font.render(self.options[i].capitalize(), 1, BLACK)
            self.SURFACE.blit(text, (i * 100 + 80 + 25 - text.get_width()/2, 15 + 25 - text.get_height()/2))
            if self.optionsBool[i][1]:
                pygame.draw.rect(self.SURFACE, BLUE, (i * 100 + 80, 15, 50, 50), 4)

class Person:
    def __init__(self, image, pos, name):
        self.name = name
        self.image = image
        self.sayings = []
        self.path = []
        self.path.append([pos[0], pos[1]])
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.POS = [self.x * 50, self.y * 50]
    def addSaying(self, saying):
        self.sayings.append(saying)
    def delSaying(self, sayingNum):
        self.sayings.pop(sayingNum)
    def addPos(self, x, y):
        self.path.append([x, y])
    def changePos(self, posNum, x, y):
        self.path[posNum] = [x, y]
    def deletePos(self, x, y):
        if [x, y] not in self.path:
            return
        for i in range(len(self.path)):
            if self.path[i] == [x, y]:
                posNum = i
        self.path.pop(posNum)

class DynamicPerson:
    def __init__(self, pos):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.inPortals = {}
        self.outPortals = {}
        self.pos = pos
        self.POS = [pos[0] * 50, pos[1] * 50]
    def addInPortal(self, x, y, portalNum):
        if portalNum in self.inPortals.keys():
            return False
        self.inPortals[portalNum] =  [x, y]
        return True
    def changeInPortal(self, x, y, portalNum):
        if portalNum not in self.inPortals.keys():
            return False
        self.inPortals[portalNum] = [x, y]
        return True
    def addOutPortal(self, x, y, portalNumThis, portalNumThat, level):
        if portalNumThis in self.outPortals.keys():
            return False
        self.outPortals[portalNumThis] = [x, y, level, portalNumThat]
        return True
    def changeOutPortal(self, x, y, portalNumThis, portalNumThat, level):
        if portalNumThis not in self.outPortals.keys():
            return False
        self.outPortals[portalNumThis] = [x, y, level, portalNumThat]
        return True
    def deleteInPortal(self, portalNum):
        self.inPortals.pop(portalNum)
    def deleteOutPortal(self, portalNum):
        self.outPortals.pop(portalNum)
    def updatePos(self, x, y):
        self.x = x
        self.y = y
        self.pos = [x, y]
        self.POS = [self.pos[0] * 50, self.pos[1] * 50]
        
class RightSidebar:
    def __init__(self):
        self.width = 80
        self.height = SCREEN_H
        self.x = SCREEN_W
        self.y = 0
        self.SURFACE = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.blocks = []
        self.goingOut = False
        self.person = None
        self.dynPerson = None
        self.dynPersonOptions = ["Add Spawn", "Move Spawn", "Del Spawn", "Add Exit", "Change Exit", "Del Exit"]
        self.dynPersonBools = [False for item in self.dynPersonOptions]
        self.regPersonOptions = ["Add Mvmnt", "Del Mvmnt", "Add Saying", "Change Say", "Del Saying"]
        self.regPersonBools = [False for item in self.regPersonOptions]
        self.font = pygame.font.SysFont("Arial", 9, True, False)
        self.camera = Camera(50, SCREEN_H - 160, 0, 0)
    def draw(self):
        self.SURFACE = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.OPTSURF = pygame.Surface((50, SCREEN_H - 160), pygame.SRCALPHA)
        pygame.draw.polygon(self.SURFACE, T_BLUE, ((0, 80), (80, 0), (80, self.height), (0, self.height - 80)))
        if self.person != None:
            x = 0
            for item in self.regPersonOptions:
                THIS = pygame.Surface((50, 50), pygame.SRCALPHA)
                TEXT = self.font.render(item.upper(), 1, BLACK)
                THIS.blit(TEXT, ( 25 - TEXT.get_width()/2, 25 - TEXT.get_height()/2))
                if self.regPersonBools[x]:
                    pygame.draw.rect(THIS, T_BLUE, (0, 0, 50, 50), 4)
                self.OPTSURF.blit(THIS, (0, x * 100 + self.camera.y))
                x += 1
        elif self.dynPerson != None:
            x = 0
            for item in self.dynPersonOptions:
                THIS = pygame.Surface((50, 50), pygame.SRCALPHA)
                TEXT = self.font.render(item.upper(), 1, BLACK)
                THIS.blit(TEXT, ( 25 - TEXT.get_width()/2, 25 - TEXT.get_height()/2))
                if self.dynPersonBools[x]:
                    pygame.draw.rect(THIS, T_BLUE, (0, 0, 50, 50), 4)
                self.OPTSURF.blit(THIS, (0, x * 100 + self.camera.y))
                x += 1
        self.SURFACE.blit(self.OPTSURF, (15, 80))
    def update(self):
        if self.goingOut:
            if self.x > SCREEN_W - 80:
                self.x -= 5
        else:
            if self.x < SCREEN_W:
                self.x += 5
        self.draw()
    def scrollOut(self):
        self.goingOut = True
    def scrollIn(self):
        self.goingOut = False
    def changePerson(self, person):
        self.person = person
    def updateEvent(self, event):
        if self.person == None and self.dynPerson == None:
            return
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4:
                self.camera.sudoScroll(False, True, 0, len(BLOCKSDICT) * 100)
            elif event.button == 5:
                self.camera.sudoScroll(True, False, 0, len(BLOCKSDICT) * 100)
            elif event.button == 1:
                X = event.pos[0]
                Y = event.pos[1]
                X = X - self.x
                Y = Y - self.camera.getY() - 80
                #X, Y = self.camera.clickToCamera(X, Y)
                if X >= 15 and X <= 65:
                    if CURRENTSCREEN == PEOPLE:
                        if self.person != None:
                            for i in range(len(self.regPersonOptions)):
                                if Y >= i * 100 and Y <= i * 100 + 100:
                                    self.regPersonBools[i] = True
                                else:
                                    self.regPersonBools[i] = False
                        elif self.dynPerson != None:
                            for i in range(len(self.dynPersonOptions)):
                                if Y >= i * 100 and Y <= i * 100 + 100:
                                    self.dynPersonBools[i] = True
                                else:
                                    self.dynPersonBools[i] = False
                        if self.regPersonBools[3] and len(self.person.sayings) == 0: #if you have to change a saying, but no sayings exist
                            self.regPersonBools[3] = False #set it to false

class TopBar:
    def __init__(self):
        self.width = SCREEN_W - 160
        self.heigth = 80
        self.x = SCREEN_W/2 - self.width/2
        self.y = -80
        self.TextInput = TextBox(80, 15, self.width-160, 50)
        self.goingOut = False
        self.SURFACE = pygame.Surface((self.width, 80), pygame.SRCALPHA)
    def begin(self):
        self.goingOut = True
    def update(self):
        if self.goingOut and self.y != 0:
            self.y += 5
        elif not self.goingOut and self.y > -80:
            self.y -= 5
        self.TextInput.update()
        self.draw()
    def updateEvent(self, event):
        if event.type == KEYDOWN and event.key == K_RETURN:
            return self.TextInput.getText()
        self.TextInput.updateText(event)
    def draw(self):
        self.SURFACE = pygame.Surface((self.width, 80), pygame.SRCALPHA)
        pygame.draw.polygon(self.SURFACE, T_BLUE, ((0,0), (80, 80), (self.width-80, 80), (self.width, 0)))
        self.SURFACE.blit(self.TextInput.surface, (80, 15))
    def setText(self, text):
        self.TextInput.string = []
        for letter in text: self.TextInput.string.append(letter);
    def delText(self, text):
        self.TextInput.string = [] 
    def getText(self):
        return self.TextInput.getText()
    def end(self):
        self.goingOut = False

def main():
    global DISPLAYSURF, FPSCLOCK, FPS, topbar, FONT, CURRENTSCREEN
    
    setupPeople()
    setupBlocks()
    setUpPeopleImages()
    
    pygame.init()
    
    FONT = pygame.font.SysFont("Arial", 20, True, False)
    
    DISPLAYSURF = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    FPSCLOCK = pygame.time.Clock()
    FPS = 40
    
    width, height = getMapInfo()
    world = World(width, height)
    cam = Camera(SCREEN_W, SCREEN_H, SCREEN_W/2, SCREEN_H/2)
    render = Renderer(world)
    sidebar = LeftSidebar()
    sidebar2 = RightSidebar()
    bottombar = BottomBar(SCREEN_W/2 - 600/2, SCREEN_H, 600, 80)
    topbar = TopBar()
    
    CURRENTSCREEN = BLOCKS
    
    while True:
        #update display and make computer wait for the FPSCLOCK
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
        #check for various exiting or saving options
        if bottombar.optionsBool[2][1]:
            save(world, render, cam)
            bottombar.optionsBool[2][1] = False
            
        #draw the map from the info in the world
        render.drawMap()
        
        #DRAW EXTRA INFO
        if sidebar2.person != None:
            for i in range(len(sidebar2.person.path)):
                pygame.draw.rect(render.SURFACE, T_RED, (sidebar2.person.path[i][0] * 50, sidebar2.person.path[i][1] * 50, 50, 50), 4)
                num = FONT.render(str(i), 1, BLACK)
                render.SURFACE.blit(num, (sidebar2.person.path[i][0] * 50 + 25 - num.get_width(), sidebar2.person.path[i][1] * 50 + 25 - num.get_height()))
        elif sidebar2.dynPerson != None:
            pygame.draw.rect(render.SURFACE, T_RED, (sidebar2.dynPerson.POS[0], sidebar2.dynPerson.POS[1], 50, 50), 4)
            if sidebar2.dynPersonBools[0] or sidebar2.dynPersonBools[1] or sidebar2.dynPersonBools[2]:
                for i in range(len(world.portalsIn)):
                    numText = FONT.render(str(i + 1), 1, BLACK)
                    thisX, thisY = world.portalsIn[i+1][0], world.portalsIn[i+1][1]
                    pygame.draw.rect(render.SURFACE, T_BLUE, (thisX * 50, thisY * 50, 50, 50))
                    render.SURFACE.blit(numText, (thisX*50 + 25 - numText.get_width()/2, thisY * 50 + 25 - numText.get_height()/2))
            elif sidebar2.dynPersonBools[3] or sidebar2.dynPersonBools[4] or sidebar2.dynPersonBools[5]:
                for i in range(len(world.portalsOut)):
                    numText = FONT.render(str(i + 1), 1, BLACK)
                    thisX, thisY = eval(world.portalsOut.keys()[i])[0], eval(world.portalsOut.keys()[i])[1]
                    pygame.draw.rect(render.SURFACE, T_BLUE, ((thisX * 50), (thisY * 50), 50, 50), 4)
                    render.SURFACE.blit(numText, (thisX * 50 + 25 - numText.get_width()/2, thisY * 50 + 25 - numText.get_height()/2))

        #Fill screen then draw the different surfaces to the screen as necessary
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(render.SURFACE, cam.getPos())
        DISPLAYSURF.blit(sidebar.SURFACE, (sidebar.x, sidebar.y))
        DISPLAYSURF.blit(bottombar.SURFACE, (bottombar.x, bottombar.y))
        DISPLAYSURF.blit(sidebar2.SURFACE, (sidebar2.x, sidebar2.y))
        DISPLAYSURF.blit(topbar.SURFACE, (topbar.x, topbar.y))
        
        #update the camera and all scroll bars
        cam.update()
        sidebar.update()
        sidebar2.update()
        topbar.update()
        bottombar.update()
        
        if CURRENTSCREEN == BLOCKS:
            topbar.goingOut = False

        print pygame.mouse.get_pos()
        if pygame.mouse.get_pos()[0] >= world.width * 50 + cam.getX() and pygame.mouse.get_pos()[0] <= world.width * 50 + cam.getX() + 50:
            for x in range(world.height):
                pygame.draw.rect(DISPLAYSURF, T_BLUE, ((world.width * 50 + cam.getX()), (cam.getY() + x * 50), 50, 50), 4)
        if pygame.mouse.get_pos()[0] <= cam.getX() and pygame.mouse.get_pos()[0] >= cam.getX() - 50:
            for x in range(world.height):
                pygame.draw.rect(DISPLAYSURF, T_BLUE, ((cam.getX() - 50), (cam.getY() + x * 50), 50, 50), 4)
        if pygame.mouse.get_pos()[1] >= world.height * 50 + cam.getY() and pygame.mouse.get_pos()[1] <= world.height * 50 + cam.getY() + 50:
            for x in range(world.width):
                pygame.draw.rect(DISPLAYSURF, T_BLUE, ((x * 50 + cam.getX()), (cam.getY() + world.height * 50), 50, 50), 4)
        if pygame.mouse.get_pos()[1] <= cam.getY() and pygame.mouse.get_pos()[1] >= cam.getY() - 50:
            for x in range(world.width):
                pygame.draw.rect(DISPLAYSURF, T_BLUE, ((cam.getX() + x * 50), (cam.getY() - 50), 50, 50), 4)

                        
        for event in pygame.event.get(): #take event
                    
            if event.type == QUIT: #if 'x' is clicked
                pygame.quit() #quit pygame
                sys.exit() #exit app
                
            #################################################################################
            ##########----Anything below here is to get and utilize user input----###########
            #################################################################################
            elif event.type == MOUSEMOTION or event.type == MOUSEBUTTONDOWN: #if you use mouse at all
                if event.pos[0] <= 80: #if mouse is near the left
                    sidebar.scrollOut() #scroll out left side bar
                    sidebar.updateEvent(event) #update any events given to the sidebar
                elif event.pos[1] >= SCREEN_H - 80: #if mouse is near the bottom
                    bottombar.scrollOut() #scroll out the bottom
                    bottombar.updateEvent(event) #update any events given to the bottom bar
                    if event.type == MOUSEBUTTONDOWN: sidebar.camera.y = 0;
                elif event.pos[0] >= SCREEN_W - 80 and CURRENTSCREEN == PEOPLE: #if working with people and near the right side
                    sidebar2.scrollOut() #scroll out the right side bar
                    sidebar2.updateEvent(event) #update any events give to the right bar
                    ###################
                    #IF YOU NEED INPUT#
                    ###################
                    if sidebar2.regPersonBools[2]:
                        topbar.begin()
                        sidebar2.person.addSaying(getSaying(topbar, render, cam, sidebar2.person.sayings, True, False)[0])
                        sidebar2.regPersonBools[2] = False
                        topbar.end()
                    elif sidebar2.regPersonBools[3]:
                        topbar.begin()
                        thisText, thisNum = getSaying(topbar, render, cam, sidebar2.person.sayings, False, False)
                        sidebar2.person.sayings[thisNum] = thisText
                        sidebar2.regPersonBools[3] = False
                        topbar.end()
                    elif sidebar2.regPersonBools[4]:
                        thisText, thisNum = getSaying(topbar, render, cam, sidebar2.person.sayings, False, True)
                        sidebar2.person.delSaying(thisNum)
                        sidebar2.regPersonBools[4] = False
                    
                        
                ##########################################################################################
                ######-------Any below here is the stuff to use the main area of the screen-------########
                ##########################################################################################
                else: #mouse is in the center area of the screen
                    #scroll in all bars
                    sidebar.scrollIn() 
                    sidebar2.scrollIn()
                    bottombar.scrollIn()
                    
                    if event.type == MOUSEBUTTONDOWN and event.button == 1: #if left clicked
                        x, y = event.pos #get the pos of the mouse
                        x, y = cam.clickToCamera(x, y) #change it to the position of the camera
                        if (x >= 0 and y >= 0 and y <= len(world.map) * 50 and x <= len(world.map[0]) * 50): #if in the map area
                            
                            if CURRENTSCREEN == BLOCKS: #if working with blocks
                                world.map[y/50][x/50] = sidebar.SELECTEDBLOCK #change the map piece hovering over to the selected block
                                sidebar2.person = None #update sidebar person to None so no highlights are there
                                sidebar2.dynPerson = None #same as previous 
                                
                            elif CURRENTSCREEN == PEOPLE: #if working with people
                                if sidebar2.person == None and sidebar2.dynPerson == None: #if person  not selected
                                    CONTINUE = False
                                    
                                    for person in world.people:
                                        if person.x == x/50 and person.y == y/50:
                                            sidebar2.person = person
                                            CONTINUE = True
                                            continue
                                    if CONTINUE: continue;
                                    
                                    if world.person.x == x/50 and world.person.y == y/50:
                                        sidebar2.dynPerson = world.person
                                        continue
                                    
                                    elif sidebar.SELECTEDPERSON == PEOPLEDICT[0][0]:
                                        a = [PERS.pos for PERS in world.people]
                                        if [x/50, y/50] not in a:
                                            world.person.updatePos(x/50, y/50)
                                            
                                    elif sidebar.SELECTEDPERSON != None:
                                        world.addPerson(IMAGESDICT[sidebar.SELECTEDPERSON], [x/50, y/50], sidebar.SELECTEDPERSON)
                                        
                                else: #if person is selected to be worked with
                                    if sidebar2.dynPerson != None: #if working with main character
                                        if sidebar2.dynPersonBools[0]:#add spawn
                                            world.portalsIn[len(world.portalsIn) + 1] = [x/50, y/50]
                                        elif sidebar2.dynPersonBools[1]:#move spawn
                                            if world.selectedPortal == None:
                                                if [x/50, y/50] in world.portalsIn.values(): world.selectedPortal = str([x/50, y/50])
                                            else:
                                                reverse = {}
                                                for item in world.portalsIn.keys():
                                                    reverse[str(world.portalsIn[item])] = item
                                                world.portalsIn[reverse[str(world.selectedPortal)]] = [x/50, y/50]
                                                world.selectedPortal = None
                                        elif sidebar2.dynPersonBools[2]: #delete spawn
                                            reverse = {}
                                            for item in world.portalsIn.keys():
                                                reverse[str(world.portalsIn[item])] = item
                                            del world.portalsIn[reverse[str([x/50, y/50])]]
                                        elif sidebar2.dynPersonBools[3]: #add exit
                                            LeVeL, NuM = addExit(world, cam, render)
                                            world.portalsOut[str([x/50, y/50])] = str([LeVeL, NuM])
                                            sidebar2.dynPersonBools[3] = False
                                        elif sidebar2.dynPersonBools[4]: #move exit
                                            if world.selectedPortal == None:
                                                if str([x/50, y/50]) in world.portalsOut.keys(): world.selectedPortal = [x/50, y/50]
                                            else:
                                                reverse = {}
                                                for item in world.portalsOut.keys():
                                                    reverse[world.portalsOut[item]] = item
                                                reverse[world.portalsOut[str(world.selectedPortal)]] = str([x/50, y/50])
                                                world.portalsOut = {}
                                                for item in reverse.keys():
                                                    world.portalsOut[reverse[item]] = item
                                                sidebar2.dynPersonBools[4] = False
                                        elif sidebar2.dynPersonBools[5]: #delete exit
                                            del world.portalsOut[str([x/50, y/50])]
                                    elif sidebar2.person != None: #same story as above
                                        if sidebar2.regPersonBools[0]:
                                            sidebar2.person.path.append([x/50, y/50])
                                        elif sidebar2.regPersonBools[1]:
                                            sidebar2.person.deletePos(x/50, y/50)
                        elif event.pos[0] >= world.width * 50 + cam.getX() and event.pos[0] <= world.width * 50 + cam.getX() + 50:
                            world.addRight()
                        elif pygame.mouse.get_pos()[0] <= cam.getX() and pygame.mouse.get_pos()[0] >= cam.getX() - 50:
                            world.addLeft()
                        elif event.pos[1] >= world.height * 50 + cam.getY() and event.pos[1] <= world.height * 50 + cam.getY() + 50:
                            world.addBelow()
                        elif pygame.mouse.get_pos()[1] <= cam.getY() and pygame.mouse.get_pos()[1] >= cam.getY() - 50:
                            world.addAbove()

                                        
            ######################################################
            ####----From here down is to take input from  ----####
            ####----            the keyboard              ----####
            ######################################################
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    cam.up()
                elif event.key == K_a:
                    cam.left()
                elif event.key == K_s:
                    cam.down()
                elif event.key == K_d:
                    cam.right()
                elif event.key == K_c:
                    pygame.image.save(DISPLAYSURF, "screenshot.png")
            elif event.type == KEYUP:
                if event.key == K_w:
                    cam.up()
                elif event.key == K_a:
                    cam.left()
                elif event.key == K_d:
                    cam.right()
                elif event.key == K_s:
                    cam.down()
            
class TextBox:
    def __init__(self, x, y, width, height):
        self.x = x - width/2
        self.y = y - height/2
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.string = []
        self.focus = False
        self.toggleLength = 20
        self.currentToggle = 0
        x = 0
        while True:
            x += 1
            self.font = pygame.font.SysFont("Arial", x, True, False)
            self.textRect = self.font.render("A", 1, BLACK)
            if self.textRect.get_rect().height >= height - 10 and self.textRect.get_rect().height <= height - 5:
                break
            else:
                continue
        self.update()
    def updateText(self, Input):
        if Input.type == MOUSEBUTTONDOWN:
            if Input.pos[0] <= self.x and Input.pos[0] >= self.x + self.width:
                if Input.pos[1] <= self.y and Input.pos[1] >= self.y + self.height:
                    self.focus = False 
        if Input.type == KEYDOWN:
            if Input.key == K_BACKSPACE:
                if len(self.string) >= 1:
                    del self.string[len(self.string) - 1]
            elif Input.key == K_RETURN:
                return True
            else:
                self.string.append(Input.unicode)
        return False
        
    def update(self):
        self.currentToggle += 1
        if self.currentToggle == self.toggleLength*2:
            self.currentToggle = 0
        if self.currentToggle < self.toggleLength:
            text = self.font.render("".join(self.string), 1, (BLACK))
        else:
            if self.isFocused():
                text = self.font.render("".join(self.string) + "|", 1, BLACK)
            else:
                text = self.font.render("".join(self.string), 1, (BLACK))
            
        self.draw(text)
    def draw(self, text):
        self.surface.fill(BLUE)
        pygame.draw.rect(self.surface, GREEN, pygame.Rect(0, 0, self.width, self.height), 4)
        self.surface.blit(text, (0, 0))
    def isFocused(self):
        return self.focus
    def takeFocus(self, x, y):
        if x >= self.x and x <= self.x + self.width:
            if y >= self.y and y <= self.y + self.height:
                self.focus = not self.focus
    def toggleFocus(self):
        self.focus = not self.focus
    def getText(self):
        return "".join(self.string)

def getMapInfo():
    width = TextBox(SCREEN_W/2, SCREEN_H/2 - 50, 400, 50)
    height = TextBox(SCREEN_W/2, SCREEN_H/2 + 50, 400, 50)
    WIDTH = width.font.render("WIDTH:", 1, BLACK)
    HEIGHT = height.font.render("HEIGHT:", 1, BLACK)
    while True:
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
        DISPLAYSURF.fill(RED)
        
        DISPLAYSURF.blit(WIDTH, (width.x - WIDTH.get_width(), width.y))
        DISPLAYSURF.blit(HEIGHT, (height.x - HEIGHT.get_width(), height.y))
        DISPLAYSURF.blit(width.surface, (width.x, width.y))
        DISPLAYSURF.blit(height.surface, (height.x, height.y))
        
        if width.isFocused():
            width.update()
        elif height.isFocused():
            height.update()
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    try:
                        if int(width.getText()) > 5:
                            if int(height.getText()) > 5:
                                return (int(height.getText()), int(width.getText()))
                    except:
                        continue
                elif event.key == K_TAB:
                    if width.isFocused():
                        width.toggleFocus()
                        width.update()
                        height.toggleFocus()
                    elif height.isFocused():
                        height.toggleFocus()
                        height.update()
                        width.toggleFocus()
                    else:
                        width.toggleFocus()
                else:
                    if width.isFocused():
                        width.updateText(event)
                    elif height.isFocused():
                        height.updateText(event)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                width.takeFocus(event.pos[0], event.pos[1])
                height.takeFocus(event.pos[0], event.pos[1])

def save(world, render, cam):
    POPUP = pygame.Surface((SCREEN_W/2, SCREEN_H/2), pygame.SRCALPHA)
    FILENAME = TextBox(POPUP.get_width()/2, 40, POPUP.get_width()/2, 50)
    FILENAME.toggleFocus()
    OPTIONS = ["save", "save and exit", "cancel"]
    X = SCREEN_W/2 - POPUP.get_width()/2
    Y = SCREEN_H/2 - POPUP.get_height()/2
    HIGHLIGHT = None
    while True:
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
        #update the screen
        POPUP = pygame.Surface((SCREEN_W/2, SCREEN_H/2), pygame.SRCALPHA)
        POPUP.fill(T_BLUE)
        TEXT = FONT.render("LEVEL:", 1, BLACK)
        POPUP.blit(TEXT, (FILENAME.x - 75, FILENAME.y + FILENAME.height/2 - TEXT.get_height()/2))
        for i in range(len(OPTIONS)):
            TEXT = FONT.render(OPTIONS[i].upper(), 1, BLACK)
            POPUP.blit(TEXT, (POPUP.get_width()/2 - TEXT.get_width()/2, i * 50 + 100))
        if HIGHLIGHT != None: pygame.draw.rect(POPUP, BLACK, HIGHLIGHT, 4);
        POPUP.blit(FILENAME.surface, (FILENAME.x, FILENAME.y))
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(render.SURFACE, cam.getPos())
        DISPLAYSURF.blit(POPUP, (X, SCREEN_H/2 - POPUP.get_height()/2))
        
        #update the FILENAME
        FILENAME.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                x, y = event.pos
                if x >= SCREEN_W/2 - 100 and x <= SCREEN_W/2 + 100:
                    if y >= Y + 100 and y <= Y + 150:
                        HIGHLIGHT = (POPUP.get_width()/2 - 100, 100 - 20, 200, 50)
                    elif y >= Y + 150 and y <= Y + 200:
                        HIGHLIGHT = (POPUP.get_width()/2 - 100, 150 - 20, 200, 50)
                    elif y >= Y + 200 and y <= Y + 250:
                        HIGHLIGHT = (POPUP.get_width()/2 - 100, 200 - 20, 200, 50)
            elif event.type == MOUSEBUTTONDOWN:
                if x >= SCREEN_W/2 - 100 and x <= SCREEN_W/2 + 100:
                    name = FILENAME.getText()
                    if y >= Y + 200 and y <= Y + 250:
                        return
                    try:
                        int(name)
                    except:
                        continue
                    if y >= Y + 100 and y <= Y + 150:
                        if name != None:
                            saveFile(world, name)
                            return
                    elif y >= Y + 150 and y <= Y + 200:
                        if name != None:
                            saveFile(world, name)
                            pygame.quit()
                            sys.exit()
                    else:
                        FILENAME.toggleFocus()
            else:
                FILENAME.updateText(event)
        
def saveFile(world, name):
    foo = open(CWDF + ('level' + str(name) + '.txt'), 'w')
    foo.write("")
    foo.close()
    foo = open(CWDF + ('level' + str(name) + '.txt'), 'a')
    LINES_TO_WRITE = []
    allPeople = []
    #get info for writing
    totalLines = len(world.map)
    totalPeople = len(world.people)
    for person in world.people:
        allPeople.append("['%s', %s, %s, %s]" % (person.name, person.pos, person.sayings, person.path))
        
    #write info to the file
    LINES_TO_WRITE.append("#1")
    LINES_TO_WRITE.append(str(totalLines))
    for line in world.map:
        LINES_TO_WRITE.append("".join(line))
    LINES_TO_WRITE.append("%s" % totalPeople)
    for person in allPeople:
        LINES_TO_WRITE.append(person)
    LINES_TO_WRITE.append("%s" % world.portalsIn)
    LINES_TO_WRITE.append("%s" % world.portalsOut)
    
    for line in LINES_TO_WRITE:
        foo.write(line)
        foo.write("\n")
    foo.close()

def compileAll():
    print "yay"
    
def setUpPeopleImages():
    allPeople = pygame.image.load(CWDI + "people.png")
    peopleOnImage = ['ASH', 'ZACK', 'WHITEHAIR', 'MAILMAN', 'MAILWOMAN', 
                     'FLORIST', 'SWIMMER', 'ATHLETE', 'NURSE', 'SHELBY', 
                     'DAD', 'MOM', 'MARY', 'BUGWOMAN', 'CATWOMAN', 
                     'MARY2', 'PURPLEHAIR', 'SENSEI', 'KADE', 'ALEX',
                     'PROFESSOR', 'JACK', 'CLAIRE', 'LINK', 'LINKPURPLE']
    peopleLetters = ['a', 'b', 'c', 'd', 'e',  'g', 'h', 'i', 'j', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'aa']
    for i in range(len(peopleOnImage)):
        PEOPLEDICT.append([peopleOnImage[i], peopleLetters[i]])
        PEOPLEDICT2[peopleLetters[i]] = peopleOnImage[i]
        PEOPLEOPTIONS.append(False)
    for y in range(allPeople.get_height()/200):
        for x in range(allPeople.get_width()/200):
            surf = pygame.Surface((50, 50), pygame.SRCALPHA)
            surf.blit(allPeople, (0, 0), (200 * x, 200 * y, 50, 50))
            IMAGESDICT[peopleOnImage[x + y * allPeople.get_width()/200]] = surf

def getSaying(topbar, renderer, cam, sayings, add, delete):
    if sayings == None: sayings = []
    
    thisNum = 0
        
    SAYINGSSURF = pygame.Surface((400, len(sayings) * 50 + 100), pygame.SRCALPHA)
    SAYINGSSURF.fill(T_BLUE)
    
    SAYINGSX = SCREEN_W/2 - SAYINGSSURF.get_width()/2
    SAYINGSY = SCREEN_H/2 - SAYINGSSURF.get_height()/2
    
    topbar.setText([])
    
    for i in range(len(sayings)):
        if i == 0 and not add: topbar.setText(sayings[i])
        saying = FONT.render("%s: %s" %(i + 1, sayings[i]), 1, BLACK)
        SAYINGSSURF.blit(saying, (10, i * 50 + 50))
            
    while True:
        FPSCLOCK.tick(FPS)
        pygame.display.update()
        
        topbar.update()
        renderer.drawMap()
        
        DISPLAYSURF.blit(renderer.SURFACE, (cam.x, cam.y))
        DISPLAYSURF.blit(topbar.SURFACE, (topbar.x, topbar.y))
        DISPLAYSURF.blit(SAYINGSSURF, (SAYINGSX, SAYINGSY))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return topbar.getText(), thisNum
                else:
                    topbar.updateEvent(event)
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if x > SAYINGSX and x < SAYINGSX + SAYINGSSURF.get_width():
                    if y > SAYINGSY and y < SAYINGSY + SAYINGSSURF.get_height():
                        x -= SAYINGSX
                        y -= SAYINGSY
                else:
                    continue
                for i in range(len(sayings)):
                    if y > i * 50 + 50 and y < i * 50 + 100:
                        if delete:
                            return topbar.getText(), i
                        elif not add:
                            thisNum = i
                            topbar.setText(sayings[i])
    
def addExit(world, cam, renderer):
    EXTRALEVELMAP = []
    ExtraLevelSpawn = dict()
    REVERSESPAWNS = {V:K for K,V in ExtraLevelSpawn}
    LEVEL = 0
    def loadExtraLevel(level):
        foo = open(CWDF + 'level%s.txt' % (level), 'r')
        foo.readline()
        numOfLines = int(foo.readline())
        for i in range(numOfLines):
            line = []
            LINE = foo.readline().strip("\n")
            for letter in LINE:
                line.append(letter)
            EXTRALEVELMAP.append(line)
        numToSkip = int(foo.readline())
        for x in range(numToSkip):
            foo.readline()
        thisLine = eval(foo.readline())
        for K in thisLine.keys():
            ExtraLevelSpawn[K] = thisLine[K]
        foo.close()
        if len(ExtraLevelSpawn) == 0:
            return False
        return True
    
    options = []
    
    for item in os.listdir(CWDF):
        item = item.strip(".txt")
        item = item.upper()
        options.append(item)
        
    optionsBool = [False for item in options]
    
    camera = Camera(350, 500, 0, 0)
    camera.y = 0
    
    OKSURF = pygame.Surface((350, 50), pygame.SRCALPHA)
    OKSURF.fill(T_BLUE)
    
    class ExternalWorld:
        def __init__(self, Map, spawns):
            self.map = Map
            self.spawns = spawns
            self.SURFACE = pygame.Surface((len(self.map[0]) * 50, len(self.map) * 50))
            self.draw()
        def draw(self):
            for y in range(len(self.map)):
                for x in range(len(self.map[0])):
                    letter = self.map[y][x]
                    if letter == "r":
                        self.SURFACE.blit(IMAGESDICT["grass"], (x * 50, y * 50))
                        self.SURFACE.blit(IMAGESDICT["rock"], (x * 50, y * 50))
                    elif letter == "t":
                        self.SURFACE.blit(IMAGESDICT["grass"], (x * 50, y * 50))
                        self.SURFACE.blit(IMAGESDICT["short tree"], (x * 50, y * 50))
                    elif letter == "b":
                        self.SURFACE.blit(IMAGESDICT["grass"], (x * 50, y * 50))
                        self.SURFACE.blit(IMAGESDICT["bush"], (x * 50, y * 50))
                    elif letter == "w":
                        self.SURFACE.blit(IMAGESDICT["grass"], (x * 50, y * 50))
                        self.SURFACE.blit(IMAGESDICT["wall"], (x * 50, y * 50 - 30))
                    else:
                        self.SURFACE.blit(IMAGESDICT[BLOCKSDICT2[letter]], (x * 50, y * 50))
            for K in self.spawns.keys():
                textNum = FONT.render(str(K), 1, BLACK)
                self.SURFACE.blit(textNum, (self.spawns[K][0] * 50 + 25 - textNum.get_width()/2, self.spawns[K][1] * 50 + 25 - textNum.get_height()/2))
                pygame.draw.rect(self.SURFACE, T_BLUE, (self.spawns[K][0] * 50, self.spawns[K][1] * 50, 50, 50), 4)
    def getFile():
        while True:
            BREAK = False
            FPSCLOCK.tick(FPS)
            pygame.display.update()
            
            DECISIONSURF = pygame.Surface((600, 400), pygame.SRCALPHA)
            DECISIONSURF.fill(T_BLUE)
            
            OPTIONSSURF = pygame.Surface((350, 500), pygame.SRCALPHA)
            for i in range(len(options)):
                OPTIONSSURF.blit(FONT.render(options[i], 1, BLACK), (25, i * 50 + camera.y))
                if optionsBool[i]: pygame.draw.rect(OPTIONSSURF, BLUE, (0, i * 50 + camera.y, camera.width, 25), 4)
            OK = FONT.render("OK", 1, BLACK)
            DECISIONSURF.blit(OK, (DECISIONSURF.get_width()/2 - OK.get_width()/2, DECISIONSURF.get_height()-25 -OK.get_width()/2))
            pygame.draw.rect(DECISIONSURF, BLUE, (25, DECISIONSURF.get_height() - 50, DECISIONSURF.get_width()-50, 50), 4)
            DECISIONSURF.blit(OPTIONSSURF, (25, 50))
            DISPLAYSURF.blit(DECISIONSURF, (100, 100))
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    x = x - 100
                    y = y - 150
                    if x >= 25 and x <= DECISIONSURF.get_width() - 25:
                        if y >= 0 and y <= DECISIONSURF.get_height() - 100:
                            for i in range(len(options)):
                                if y >= i * 50 and y <= i * 50 + 50:
                                    optionsBool[i] = True
                                else:
                                    optionsBool[i] = False
                        else:
                            for i in range(len(options)):
                                if optionsBool[i]:
                                    LOADEDFILE = loadExtraLevel(int(options[i][len(options[i]) - 1]))
                                    LEVEL = int(options[i][len(options[i]) - 1])
                                    if not LOADEDFILE:
                                        return False, LEVEL
                                    BREAK = True
            if BREAK: break;
        return True, LEVEL
    def getSpawn():
        externalworld = ExternalWorld(EXTRALEVELMAP, ExtraLevelSpawn)
        WDOWN = False
        ADOWN = False
        SDOWN = False
        DDOWN = False
        offsetX = 0
        offsetY = 0
        while True:
            FPSCLOCK.tick(FPS)
            pygame.display.update()
            
            DISPLAYSURF.fill(WHITE)
            DISPLAYSURF.blit(externalworld.SURFACE, (offsetX, offsetY))
            
            if WDOWN: offsetY -= 5
            if ADOWN: offsetX -= 5
            if SDOWN: offsetY += 5
            if DDOWN: offsetX += 5
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        x = x - offsetX
                        y = y - offsetY
                        if [x/50, y/50] in ExtraLevelSpawn.values():
                            for item in ExtraLevelSpawn.items():
                                if item[1] == [x/50, y/50]: return item[0]
                elif event.type == KEYDOWN:
                    if event.key == K_w:
                        WDOWN = True
                    elif event.key == K_a:
                        ADOWN = True
                    elif event.key == K_s:
                        SDOWN = True
                    elif event.key == K_d:
                        DDOWN = True
                elif event.type == KEYUP:
                    if event.key == K_w:
                        WDOWN = False
                    elif event.key == K_a:
                        ADOWN = False
                    elif event.key == K_s:
                        SDOWN = False
                    elif event.key == K_d:
                        DDOWN = False
            
    FILEEXISTS, LEVEL = getFile()
    if FILEEXISTS:
        num = getSpawn()
        return LEVEL, num
    return None

if __name__ == "__main__":
    main()
