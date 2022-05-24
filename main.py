
from RaceTrack import*
from CarLineage import*
from Car import*



#start the pygame engine
pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont('Comic Sans MS', 23)
myfont2 = pygame.font.SysFont('arial.ttf', 20)


FPS = 60
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720))
gen_count = 1

player1 = Car(100,100)
carList = CarLineage(400, 200)
track1 = RaceTrack("track 1")

def getUserInput():
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_a]:
        player1.rotateLeft(track1.getWalls())
    elif pressed[pygame.K_d]:
        player1.rotateRight(track1.getWalls())
    if pressed[pygame.K_w]:
        player1.move(track1)
    elif pressed[pygame.K_s]:
        player1.reverse(track1.getWalls())

def drawScore():
    for car in carList.getCarList():
        textsurface = myfont2.render(str(car.getScore()), False, (0, 0, 0))
        screen.blit(textsurface, (car.getX() + 3, car.getY() + 10))

def drawHUD():
    textsurface = myfont.render("check point 0: " + str(player1.getCheckPoint(0)), False, (0, 0, 0))
    screen.blit(textsurface,(900,0))
    textsurface = myfont.render("check point 1: " + str(player1.getCheckPoint(1)), False, (0, 0, 0))
    screen.blit(textsurface,(900,30))
    textsurface = myfont.render("check point 2: " + str(player1.getCheckPoint(2)), False, (0, 0, 0))
    screen.blit(textsurface,(900,60))
    textsurface = myfont.render("check point 3: " + str(player1.getCheckPoint(3)), False, (0, 0, 0))
    screen.blit(textsurface,(900,90))
    textsurface = myfont.render("check point 4: " + str(player1.getCheckPoint(4)), False, (0, 0, 0))
    screen.blit(textsurface,(900,120))
    textsurface = myfont.render("Laps: " + str(carList.getMaxLap()), False, (0, 0, 0))
    screen.blit(textsurface,(900,150))
    textsurface = myfont.render("Gear: " + str(player1.getGear()), False, (0, 0, 0))
    screen.blit(textsurface,(900,180))
    textsurface = myfont.render("Generation: " + str(gen_count), False, (0, 0, 0))
    screen.blit(textsurface,(900,210))

def update():
    carList.updateLeaderBoard()
    for car in carList.getCarList():
        car.updateTimeDict()

def clear_screen():
    pygame.draw.rect(screen, (240,224,202), (0, 0, 1280, 720))

def createTrack1():
    track1.addRect(pygame.Rect(0,0,800,25))
    track1.addRect(pygame.Rect(800,0,25,325))
    track1.addRect(pygame.Rect(810,300,300,25))
    track1.addRect(pygame.Rect(1100,300,25,300))
    track1.addRect(pygame.Rect(0,600,1125,25))
    track1.addRect(pygame.Rect(0,0,25,600))
    track1.addRect(pygame.Rect(200,200,400,25))
    track1.addRect(pygame.Rect(200,200,25,250))
    track1.addRect(pygame.Rect(600,200,25,200))
    track1.addRect(pygame.Rect(600,400,150,25))
    track1.addRect(pygame.Rect(750,400,25,100))
    track1.addRect(pygame.Rect(200,400,400,25))

    track1.addCheckPoint(pygame.Rect(500,0,25,200))
    track1.addCheckPoint(pygame.Rect(600,300,200,25))
    track1.addCheckPoint(pygame.Rect(500,425,25,200))
    track1.addCheckPoint(pygame.Rect(0,400,200,25))
    track1.addCheckPoint(pygame.Rect(0,200,200,25))


createTrack1()

while True:
    #loop through and empty the event queue, key presses
    #buttons, clicks, etc.
    for event in pygame.event.get():
        #if the event is a click on the "X" close button
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player1.shiftGearUp()
            if event.key == pygame.K_DOWN:
                player1.shiftGearDown()

    getUserInput()

    clear_screen()
    track1.drawRaceTrack(screen)
    player1.draw(screen)
    carList.drawCars(screen)
    drawScore()
    carList.moveCars(track1)
    #print(carList.getCar(0).getCurrentDNA())

    drawHUD()
    pygame.display.flip()
    fpsClock.tick(FPS)
    if carList.getCar(0).getCurrentDNA() == 200:
        carList.createNewGeneration()
        gen_count+=1
        carList.resetCars()

