import random
import math
import pygame
import time

#changed two things:
    #removed collision detection on changing of angle, the car can ALWAYS rotate now
    #changed collision detection to check which side of car is colliding and allowing it to continue moving
    #    in the opposite axis of the collision


class Car:

    new_rect = pygame.Rect(0,0,1,1)

    #constructor
    def __init__(self, x, y):
        self.checkPoints = [False, False, False, False, False]
        self.x = x
        self.y = y
        self.score = 0
        self.width = 10
        self.length = 15
        self.angle = 0
        self.speed = 3
        self.numlaps = 0
        self.gear = .3
        self.lastCheck = False
        self.timeDict = {}
        self.startTime = time.time()
        self.checkPointCounted = False
        loadImage = pygame.image.load("newCar.png")
        var = pygame.PixelArray(loadImage)
        var.replace((0,255,30), (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        del var
        self.image = pygame.transform.scale(loadImage,(15,15))
        self.myRect = pygame.Rect(self.x, self.y, self.width, self.length)

    """def updateTimeDict(self):
        count = 1
        for checkpoint in self.checkPoints:
            if checkpoint and count not in self.timeDict:
                self.endTime = time.time()
                self.timeDict[count] = self.endTime - self.startTime
                self.startTime = time.time()
                count += 1"""

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getGear(self):
        return self.gear

    def getScore(self):
        return self.score

    def shiftGearUp(self):
        if self.gear < 1.2:
            self.gear += .3

    def shiftGearDown(self):
        if self.gear > .6:
            self.gear -= .3

    def getNumLaps(self):
        return self.numlaps

    def setNumLaps(self,lap):
        self.numlaps = lap

    def rotateLeft(self, track):
        oldAngle = self.angle
        self.angle = (self.angle+3) % 360
        #for rectangle in track:
        #    if pygame.Rect.colliderect(rectangle, self.new_rect):
        #        self.angle = oldAngle

    def canRotateLeft(self, track):
        oldAngle = self.angle
        self.angle+=3
        for rectangle in track:
            if pygame.Rect.colliderect(rectangle, self.new_rect):
                self.angle = oldAngle
                return False
        self.angle = oldAngle
        return True

    def getCheckPoint(self, n):
        if(n < len(self.checkPoints)):
            return self.checkPoints[n]
        else:
            return "BAD DATA"

    def rotateRight(self, track):
        oldAngle = self.angle
        self.angle-=3
        if(self.angle < 0):
            self.angle = 359
        #for rectangle in track:
        #    if pygame.Rect.colliderect(rectangle, self.new_rect):
        #        self.angle = oldAngle

    def canRotateRight(self, track):
        oldAngle = self.angle
        self.angle-=3
        for rectangle in track:
            if pygame.Rect.colliderect(rectangle, self.new_rect):
                self.angle = oldAngle
                return False
        self.angle = oldAngle
        return True

    def reverse(self, track):
        if not self.canMove(track) or not self.canRotateRight(track) or not self.canRotateLeft(track):
            self.x -= self.speed * math.sin((self.angle+90)/180*math.pi)
            self.y -= self.speed * math.cos((self.angle+90)/180*math.pi)

    def move(self, track):
        if self.numlaps > 0:
            print(self.numlaps)
        oldx = self.x
        oldy = self.y
        walls = track.getWalls()
        trackCheckPoints = track.getCheckPoints()
        self.x += self.gear * self.speed * math.sin((self.angle+90)/180*math.pi)
        self.y += self.gear * self.speed * math.cos((self.angle+90)/180*math.pi)
        for rectangle in walls:
            if pygame.Rect.colliderect(rectangle, self.new_rect):
                #hitting top
                if abs(self.new_rect.y - (rectangle.y + rectangle.height)) < 5:
                    self.y = rectangle.y+rectangle.height+10
                #hitting bottom
                elif abs((self.new_rect.y + self.new_rect.height) - rectangle.y) < 5:
                    self.y = rectangle.y-10
                #hitting left
                elif abs(self.new_rect.x - (rectangle.x + rectangle.width)) < 5:
                    self.x = rectangle.x+rectangle.width+10
                #hitting right
                elif abs((self.new_rect.x+self.new_rect.width) - rectangle.x) < 5:
                    self.x = rectangle.x-10
        for i in range(0,len(trackCheckPoints)):
            if pygame.Rect.colliderect(trackCheckPoints[i],self.new_rect):
                if i == 0 and self.checkPoints[0] == False:
                    self.checkPoints[0] = True
                    self.score += 1
                    if self.lastCheck:
                        self.numlaps += 1
                        self.lastCheck = False
                else:
                    if self.checkPoints[i-1] == True and self.checkPoints[i] == False:
                        self.checkPoints[i] = True
                        self.score += 1
                    if i == 4:
                        if self.checkPoints[3]:
                            print("Yes")
                            self.checkPoints[4] = True
                            #self.numlaps += 1
                            self.lastCheck = True
                        self.checkPoints[0] = False
                        self.checkPoints[1] = False
                        self.checkPoints[2] = False
                        self.checkPoints[3] = False
                        self.checkPoints[4] = False

    def canMove(self, track):
        oldx = self.x
        oldy = self.y
        self.x += self.speed * math.sin((self.angle+90)/180*math.pi)
        self.y += self.speed * math.cos((self.angle+90)/180*math.pi)
        for rectangle in track:
            if pygame.Rect.colliderect(rectangle, self.new_rect):
                self.x = oldx
                self.y = oldy
                return False
        self.x = oldx
        self.y = oldy
        return True

    def draw(self, screen):
        rotatedImage = pygame.transform.rotate(self.image,self.angle)
        self.new_rect = rotatedImage.get_rect(center = self.image.get_rect(center = (self.x, self.y)).center)
        screen.blit(rotatedImage, self.new_rect)


