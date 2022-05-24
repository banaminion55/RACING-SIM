import copy
from aiCar import*
import time

class CarLineage:

    def __init__(self, generationSize, dnaLength):
        self.carList = [aiCar(100,100,dnaLength) for i in range(generationSize)]
        self.generationSize = generationSize
        self.dnaLength = dnaLength
        self.leaderBoardDict = {}


    def getCarList(self):
        return self.carList

    def getCar(self, index):
        return self.carList[index]

    def drawCars(self, screen):
        for car in self.carList:
            car.draw(screen)

    def resetCars(self):
        for car in self.carList:
            car.reset()
            car.setPosition(100, 100)
            car.setNumLaps(0)

    def moveCars(self, track):
        for car in self.carList:
            car.move(track)

    def sortCars(self):
        self.carList = sorted(self.carList,key=lambda x: x.getScore(), reverse=True)

    def createNewDNA(self,fatherDNA,motherDNA,cutoff):
        newDNA = []
        for i in range(cutoff):
            a = random.randint(1,100)
            if a < 4:
                newDNA.append(self.mutate())
            else:
                newDNA.append(fatherDNA[i])
        for i in range(cutoff,self.dnaLength):
            a = random.randint(1, 100)
            if a < 4:
                newDNA.append(self.mutate())
            else:
                newDNA.append(motherDNA[i])
        return newDNA


    def createNewGeneration(self):
        self.sortCars()
        babyCars = []
        for i in range(self.generationSize//2):
            self.carList.pop()
        for i in range(self.generationSize//2):
            babyCar = aiCar(100,100,self.dnaLength)
            cutoff = random.randint(0,self.dnaLength)
            maleCar = self.carList[random.randint(0,len(self.carList)-1)]
            femaleCar = self.carList[random.randint(0,len(self.carList)-1)]
            newDNA = self.createNewDNA(maleCar.getDNA(), femaleCar.getDNA(),cutoff)
            babyCar.setDNA(newDNA)
            babyCars.append(babyCar)
        for i in range(self.generationSize//2):
            self.carList.append(babyCars[i])

    def createBetterGeneration(self):
        self.sortCars()
        babyCars = []
        for i in range(self.generationSize // 2):
            self.carList.pop()
        for key in self.leaderBoardDict:
            for car in self.leaderBoardDict.get(key):
                if car not in self.carList:
                    self.carList.pop()
                    self.carList.append(car)
        for i in range(self.generationSize//2):
            babyCar = aiCar(100,100,self.dnaLength)
            cutoff = random.randint(0,self.dnaLength)
            maleCar = self.carList[random.randint(0,len(self.carList)-1)]
            femaleCar = self.carList[random.randint(0,len(self.carList)-1)]
            newDNA = self.createNewDNA(maleCar.getDNA(), femaleCar.getDNA(),cutoff)
            babyCar.setDNA(newDNA)
            babyCars.append(babyCar)
        for i in range(self.generationSize//2):
            self.carList.append(babyCars[i])

    def mutate(self):
        a = random.randint(1,100)
        if a <= 14:
            return 0
        elif a <= 32:
            return 1
        elif a <= 50:
            return 2
        elif a <= 75:
            return 3
        elif a <= 100:
            return 4

    def getMaxLap(self):
        self.sortCars()
        return self.carList[0].getNumLaps()
        """maxLap = 0
        for car in self.carList:
            if car.getNumLaps() > maxLap:
                maxLap = car.getNumLaps()
        return maxLap"""

    def updateLeaderBoard(self):
        count = 1
        carsDoneWithLap = 0
        self.sortCars()
        for car in self.carList:
            if carsDoneWithLap == 10:
                self.leaderBoardDict[count] = []
                for car in self.carList:
                    if count in car.timeDict:
                        self.leaderBoardDict[count].append(car)
                for car in self.carList:
                    car.checkPointCounted = False
                count += 1
                carsDoneWithLap = 0
            if car.getScore() == count and not car.checkPointCounted:
                carsDoneWithLap += 1
                car.checkPointCounted = True

    #def createBestGeneration(self):
















