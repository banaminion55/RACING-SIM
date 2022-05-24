
from Car import*
from CarLineage import*
import time


class aiCar(Car):

    movementDelay = 100 #ms
    nextMove = 0
    currentDNA = 0

    def __init__(self, x, y, dnaLength):
        Car.__init__(self,x,y)
        self.dna = []
        self.dnaLength = dnaLength
        self.nextMove = pygame.time.get_ticks()+self.movementDelay
        self.createDNA()


    def getCurrentDNA(self):
        return self.currentDNA

    def setPosition(self,x,y):
        self.x = x
        self.y = y
        self.gear = .3
        self.angle = 0

    def reset(self):
        self.currentDNA = 0
        self.checkPoints = [False, False, False, False, False]
        self.score = 0

    def setDNA(self, newDNA):
        self.dna = newDNA

    def getDNA(self):
        return self.dna

    def rotateRight(self,track):
        oldAngle = self.angle
        self.angle -= 10
        if (self.angle < 0):
            self.angle = 359

    def rotateLeft(self, track):
        oldAngle = self.angle
        self.angle = (self.angle+10) % 360



    def move(self, track):
        #if it's time for me to have an action
        if self.nextMove < pygame.time.get_ticks() and self.currentDNA < self.dnaLength:
            if self.dna[self.currentDNA] == 1:
                super().shiftGearUp()
            elif self.dna[self.currentDNA] == 2:
                super().shiftGearDown()
            elif self.dna[self.currentDNA] == 3:
                self.rotateLeft(track)
            elif self.dna[self.currentDNA] == 4:
                self.rotateRight(track)
            self.nextMove = pygame.time.get_ticks() + self.movementDelay
            self.currentDNA += 1

        super().move(track)


    def createDNA(self):
        for i in range(self.dnaLength):
            a = random.randint(1,100)
            if(a <= 14):
                self.dna.append(0)
            elif a <= 32:
                self.dna.append(1)
            elif a <= 50:
                self.dna.append(2)
            elif a <= 75:
                self.dna.append(3)
            elif a <= 100:
                self.dna.append(4)




