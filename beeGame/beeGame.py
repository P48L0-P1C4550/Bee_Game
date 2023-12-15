import pygame, os, time, random
pygame.init()
pygame.mixer.init()
print("a game made by Paweł Herok")

pygame.display.set_caption("Bee game")
screen = pygame.display.set_mode((1200,800))

bee1surface = pygame.image.load("bee1.png").convert_alpha()
bee2surface = pygame.image.load("bee2.png").convert_alpha()
bee3surface = pygame.image.load("bee3.png").convert_alpha()
bee4surface = pygame.image.load("bee4.png").convert_alpha()
treeStumpSurface = pygame.image.load("stump.png").convert_alpha()
bgSurface = pygame.image.load("bg.png")
menuSurface = pygame.image.load("menu.png")
deathSurface = pygame.image.load("ded.png")
turboFrameSurface = pygame.image.load("turboRamka.png").convert_alpha()
turboBarSurface = pygame.image.load("turbobar.png").convert_alpha()
bgMusic = pygame.mixer.Sound('bgMusic.mp3')
pixelFont = pygame.font.Font("bee1.ttf", 50)

#read settings file
with open("sett.txt", "r") as f:
    displayHighscore = str(f.readline())
    beeXspeed = int(f.readline())
if displayHighscore == "T\n":
    displayHighscore = True
else:
    displayHighscore = False

#all variables etc
reset = True # I want to have all reset info like high score saved from start
gamemode = "menu"

stumpY = -1000
stumpTopOrDown = 1

turboDelay = 250
tClicked = False

beeX = 600
beeY = 400

beeForceY = 0

direction = "f" # "f" - forward, "b" - backward

highscore = 0
score = 0
toBeScoreCounter = 0

keySpaceDelay = 4
canPressSpace = True

isDead = False

beeState = True # True -> frame 1;  False -> frame 2;   (animation)

#functions

def beeGravity(beeForceY,beeY):
    #gravity
    beeForceY += 1 #addition means going down the screen
    beeY += beeForceY
    beeY = round(beeY,1)
    return beeForceY, beeY

def renderBee(direction, beeState, beeY, beeX, bee1surface, bee2surface, bee3surface, bee4surface):
    #render bee
    if direction == "f":
        if beeState:
           screen.blit(bee3surface, (beeX - 50,beeY - 50))
           beeState = False
        else:
           screen.blit(bee4surface, (beeX - 50,beeY - 50))
           beeState = True
    elif direction == "b":
        if beeState:
           screen.blit(bee1surface, (beeX - 50,beeY - 50))
           beeState = False
        else:
           screen.blit(bee2surface, (beeX - 50,beeY - 50))
           beeState = True

    return beeState

def renderScore(isDead, score, toBeScoreCounter):
    if not isDead:
        toBeScoreCounter += 1
        if toBeScoreCounter == 20:
            toBeScoreCounter = 0
            score += 1
        scoreSurface = pixelFont.render(str(score), False, "Black")
    else:
        scoreSurface = pixelFont.render(str(score), False, "White")
    screen.blit(scoreSurface, (int(600 - 25 * len(str(score))),100))
    return score, toBeScoreCounter

def buttonCheck(isDead, beeForceY, canPressSpace, reset, tClicked):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            os.system("exit")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if isDead:
                    reset = True
                if canPressSpace:
                    beeForceY = round(beeForceY - beeForceY / 10, 1)
                    beeForceY -= 20
                    canPressSpace = False
            if event.key == pygame.K_t:
                tClicked = True
    return beeForceY, canPressSpace, reset, tClicked

def inRectangle(inX,inY,leftX,rightX,upperY,downY):
    if inX > leftX and inX < rightX and inY > upperY and inY < downY:
        return True
    else:
        return False
    

print()
try:
    with open("high.txt", "x") as f:
        print("file made")
except:
    print("file exists")
with open("high.txt", "r") as f:
    try:
        highscore = int(f.readline())
    except:
        print("could not read highscore")
for x in range(40):
    time.sleep(0.01)
    screen = pygame.display.set_mode((1200,x*20))

bgMusic.play()

while True:
    # ======================================================== MENU =============================================================
    
    while gamemode == "menu":
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os.system("exit")
            if event.type == pygame.MOUSEBUTTONUP:
                cursorX, cursorY = pygame.mouse.get_pos()
                # - check if minigame
                if inRectangle(cursorX,cursorY,100,400,300,400):
                    gamemode = "minigame"
                if inRectangle(cursorX,cursorY,100,400,500,600):
                    gamemode = "normal"
        screen.blit(menuSurface, (0,0))
        
        pygame.display.set_caption("Bee game - menu")
        pygame.display.update()
    # ====================================================== MINIGAME ===========================================================
    while gamemode == "minigame":
        # - reset - minigame

        if reset:
            beeY = 400
            beeX = 600
            beeForceY = 0
            score = 0
            keySpaceDelay = 4
            toBeScoreCounter = 0
            direction = "f"
            stumpY = -1000
            turboDelay = 250
            stumpTopOrDown = 1
            turbo = 0
            
            if isDead:
                keySpaceDelay = 8
            
            tClicked = False
            reset = False
            isDead = False
            renderStump = False
        
        # - button check
        beeForceY, canPressSpace, reset, tClicked = buttonCheck(isDead, beeForceY, canPressSpace, reset, tClicked)
        
        # - also check for turbo event
        turboDelay += 1
        if tClicked:
            tClicked = False
            if turboDelay >= 250:
                turboDelay = 0
                turbo = 45
        if turbo > 0:
            turbo -= 1
        
        
        # - space key delay
        keySpaceDelay -= 1
        if keySpaceDelay == 0:
            keySpaceDelay = 4
            canPressSpace = True
        
        # --- render stump ---
        
        if renderStump:
            #stump x = 450, stump y = random.randint(-200,600)
            if stumpTopOrDown == 1:
                stumpY = random.randint(-300,0)
                stumpTopOrDown = 2
                print("top")
            else:
                stumpY = random.randint(200,600)
                print("down")
                stumpTopOrDown = 1
            print(stumpY)
            renderStump = False
        
        # - check if hit stump
        if beeX > 450:
            if beeX < 750:
                if beeY > stumpY:
                    if beeY < int(stumpY + 600):
                        isDead = True
        
        
        
        # - ded
        if beeY < 0 or beeY > 800:
            isDead = True
        # - save highscore
        if highscore < score:
            highscore = score
            with open("high.txt", "w") as f:
                f.write(str(score))
        # - move X
        if not isDead:
            if direction == "f":
                beeX += beeXspeed + int(turbo / 3)
            elif direction == "b":
                beeX -= beeXspeed + int(turbo / 3)
            
            # - minigame mode
        if beeX > 1200:
            direction = "b"
            renderStump = True
        if beeX < 0:
            direction = "f"
            renderStump = True
        
        #gravity
        beeForceY, beeY = beeGravity(beeForceY, beeY)
        
        #render images
        if isDead:
            screen.blit(deathSurface, (0,0))
            score, toBeScoreCounter = renderScore(isDead, score, toBeScoreCounter)
            if displayHighscore:
                highscoreSurface = pixelFont.render(str("HIGHSCORE-" + str(highscore)), False, "Grey")
                screen.blit(highscoreSurface,(10,10))
        else:
            screen.blit(bgSurface, (0,0))
            
            screen.blit(treeStumpSurface,(450,stumpY))
            
            screen.blit(turboFrameSurface, (0,0))
            if turboDelay > 250:
                screen.blit(turboBarSurface, (0, 0))
            else:
                screen.blit(turboBarSurface, (turboDelay - 250, 0))
            
            # - render bee ------ had to put it here because function slow
            if direction == "f":
                if beeState:
                   screen.blit(bee3surface, (beeX - 50,beeY - 50))
                   beeState = False
                else:
                   screen.blit(bee4surface, (beeX - 50,beeY - 50))
                   beeState = True
            elif direction == "b":
                if beeState:
                   screen.blit(bee1surface, (beeX - 50,beeY - 50))
                   beeState = False
                else:
                   screen.blit(bee2surface, (beeX - 50,beeY - 50))
                   beeState = True
            # - GUI - Graphical user interface
            score, toBeScoreCounter = renderScore(isDead, score, toBeScoreCounter)
        
        #update and some other stuff
        pygame.display.set_caption(str("Bee game - score: " + str(score)))
        pygame.display.update()
        time.sleep(0.01)
    
    # ================================================== NORMAL GAME MODE =======================================================
    
    while gamemode == "normal":
        
        # - reset
        if reset:
            beeY = 400
            beeX = 600
            beeForceY = 0
            score = 0
            keySpaceDelay = 4
            toBeScoreCounter = 0
            direction = "f"
            turboDelay = 250
            turbo = 0
            
            if isDead:
                keySpaceDelay = 8
            
            tClicked = False
            reset = False
            isDead = False
        
        # - button check
        beeForceY, canPressSpace, reset, tClicked = buttonCheck(isDead, beeForceY, canPressSpace, reset, tClicked)
        
        
        
        #  - render stuff
            #some debug and finding out
        
        if tClicked:
            tClicked = False
        
        # - gravity
        beeForceY, beeY = beeGravity(beeForceY, beeY)