#pylint: disable = C0303, C0301, C0111, R0913, E1302, C0103

import os
import sys
import math
import random
import pygame

#TODO: everything

#IDEAS
#microtransaction!!!!!!!  THE FUTURE OF GAMING, BABY!!1!!111!
#helmet/hats system (tf2 I'm coming for you)
#   shades
#   astronaut helmet
#   tophat
#propulsion images -
#   for his neutral special, he wields a gun
#   vacuum cleaner
#   legs to swim
#change shape because dough
#at the end he's cooked into a pizza (???)
#level completion - random pun

#Platform class for creation of platforms
class platform:
    #to initialize a platform object
    #left is where left of platform will spawn
    #top is where top of platform will spawn
    #width = width of platform
    #height = height of platform
    #display = pygame display, for drawing purposes
    #weight = weight of box, used for nerd math, defaults to 5
    #origin = (X, Y) where platform is initially created
    def __init__(self, display, left, top, width, height, weight = 5):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(left, top, width, height)
        self.display = display
        self.weight = weight
        self.origin = (self.left, self.top)

    #Used to draw the platform
    #orientation used to determine what way to rotate an image
    #if an image is provided, uses display.blit to draw the image in the right spot
    #otherwise, draw a rectangle of the given color, default is white
    def draw(self, orientation = 0, image = None, color = (255, 255, 255)):
        if not image is None:
            if orientation == 1:
                self.display.blit(pygame.transform.rotate(image, -90), self.hitbox)
            elif orientation == 2:
                self.display.blit(pygame.transform.rotate(image, -180), self.hitbox)
            elif orientation == 3:
                self.display.blit(pygame.transform.rotate(image, -270), self.hitbox)
            else:
                self.display.blit(image, self.hitbox)
        else:
            pygame.draw.rect(self.display, color, self.hitbox, 3)

    #detects collisions between this object's hitbox and another's
    def rectCollide(self, rectHitbox):
        return self.hitbox.colliderect(rectHitbox)

    #updates object's position and size based on addition
    def update(self, left, top, width, height):
        self.left = self.left + left
        self.top = self.top + top
        self.width = width
        self.height = height
        if self.left <= 0:
            self.left = 0
        elif self.left >= 850:
            self.left = 850

        if self.top <= 0:
            self.top = 0
        elif self.top >= 650:
            self.top = 650
        self.hitbox = pygame.Rect(self.left, self.top, self.width, self.height)
    
    #updates object's position by explicitly changing the location
    def updateCardinal(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(left, top, width, height)

class player:
    #initializes a player object
    #display = the display that the player will be drawn on
    #left = the left side of the hitbox value
    #top = the top box of the hitbox value
    #width = width of the player hitbox
    #height = height of player hitbox
    #weight = used for nerd math, defaults to 7
    #accelX = acceleration of player in the X direction, defaults to 0
    #accelY = acceleration of player in the Y direction, defaults to 0
    #friction = player's inherit resistance and drag, defaults to 0.1
    def __init__(self, display, left, top, width, height, weight = 7, accelX = 0, accelY = 0, friction = 0.1):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(left, top, width, height)
        self.display = display
        self.weight = weight
        self.accelX = accelX
        self.accelY = accelY
        self.friction = friction

    #Draws the image given to it - it's a player, so it always has an image
    def draw(self, image):
        self.display.blit(image, self.hitbox)

    #Determines collision between the player hitbox and another object's
    def rectCollide(self, rectHitbox):
        return self.hitbox.colliderect(rectHitbox)
        
    #updates player's position and size based on addition
    def update(self, left, top, width, height):
        self.left = self.left + left
        self.top = self.top + top
        self.width = width
        self.height = height
        if self.left <= -50:
            self.left = 950
        elif self.left >= 950:
            self.left = -50

        if self.top <= -50:
            self.top = 750
        elif self.top >= 750:
            self.top = -50
        self.hitbox = pygame.Rect(self.left, self.top, self.width, self.height)

    #updates player's position and size by overwriting previous position
    def updateCardinal(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.left, self.top, self.width, self.height)

#Colors!
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
TEAL = (0, 255, 255)
SPACE_PURPLE = (48, 25, 52)
SURPRISE = (random.randrange(0, 255, 1), random.randrange(0, 255, 1), random.randrange(0, 255, 1))

#Sets up pathing
thisFolder = os.path.dirname(os.path.abspath(sys.argv[0]))

#Initialization
pygame.init()
pygame.mixer.init()
#Sets number of channels that sounds can be playing from simultaneously
pygame.mixer.set_num_channels(25)

#Zounds!
collideSoundB = pygame.mixer.Sound(os.path.join(thisFolder, "sounds\\collisionNoises\\pianoB.wav"))
collideSoundC = pygame.mixer.Sound(os.path.join(thisFolder, "sounds\\collisionNoises\\pianoC.wav"))
collideSoundE = pygame.mixer.Sound(os.path.join(thisFolder, "sounds\\collisionNoises\\pianoE.wav"))
collideSoundG = pygame.mixer.Sound(os.path.join(thisFolder, "sounds\\collisionNoises\\pianoG.wav"))
collideSounds = [collideSoundB, collideSoundC, collideSoundE, collideSoundG]
backgroundSounds = []
for i in range(1, 15, 1):
    soundTemp = pygame.mixer.Sound(os.path.join(thisFolder, "sounds\\music\\track"+str(i)+".wav"))
    backgroundSounds.append(soundTemp)
springSound = pygame.mixer.Sound(os.path.join(thisFolder, "sounds\\collisionNoises\\springSFX.wav"))
doorSound = pygame.mixer.Sound(os.path.join(thisFolder, "sounds\\doors\\door2.wav"))

#Creates the screen
screen = pygame.display.set_mode((900, 700))
center = (450, 350)
#Creates the clock to tick frames
clock = pygame.time.Clock()
#Sets the max FPS to get (or something, not super sure how this works rn)
FPS = 360

#Window Name/Icon
pygame.display.set_caption("DoughNaut")
windowIcon = pygame.image.load(os.path.join(thisFolder, 'icon.png'))
pygame.display.set_icon(windowIcon)

#Title/Tutorial Images
titleImg = pygame.image.load(os.path.join(thisFolder, 'images\\misc\\titleCard.png'))
instructionsImg = pygame.image.load(os.path.join(thisFolder, 'images\\instructions\\instructions.png'))
instructionsImg2 = pygame.image.load(os.path.join(thisFolder, 'images\\instructions\\instructions2.png'))
insructionsTeal = pygame.image.load(os.path.join(thisFolder, 'images\\instructions\\instructionsTeal.png'))
instructionsGoal = pygame.image.load(os.path.join(thisFolder, 'images\\instructions\\instructionsGoal.png'))

#player
#default player image is idle
playerImg = pygame.image.load(os.path.join(thisFolder, 'images\\player\\lookcenter.png'))
#initializes all potential images for player in cardinal directions
lookCenter = pygame.image.load(os.path.join(thisFolder, 'images\\player\\lookcenter.png'))
downRight = pygame.image.load(os.path.join(thisFolder, 'images\\player\\lookdownRight.png'))
middleRight = pygame.image.load(os.path.join(thisFolder, 'images\\player\\lookmiddleRight.png'))
upRight = pygame.image.load(os.path.join(thisFolder, 'images\\player\\lookupRight.png'))
downLeft = pygame.image.load(os.path.join(thisFolder, 'images\\player\\lookdownLeft.png'))
middleLeft = pygame.image.load(os.path.join(thisFolder, 'images\\player\\lookmiddleLeft.png'))
upLeft = pygame.image.load(os.path.join(thisFolder, 'images\\player\\lookupLeft.png'))
downMiddle = pygame.image.load(os.path.join(thisFolder, 'images\\player\\lookcenterDown.png'))
upMiddle = pygame.image.load(os.path.join(thisFolder, 'images\\player\\lookcenterUp.png'))
#initializes images for the blinking of the player
blinkCenter = pygame.image.load(os.path.join(thisFolder, 'images\\player\\blinkcenter.png'))
blinkDownRight = pygame.image.load(os.path.join(thisFolder, 'images\\player\\blinkdownRight.png'))
blinkMiddleRight = pygame.image.load(os.path.join(thisFolder, 'images\\player\\blinkmiddleRight.png'))
blinkUpRight = pygame.image.load(os.path.join(thisFolder, 'images\\player\\blinkupRight.png'))
blinkDownLeft = pygame.image.load(os.path.join(thisFolder, 'images\\player\\blinkdownLeft.png'))
blinkMiddleLeft = pygame.image.load(os.path.join(thisFolder, 'images\\player\\blinkmiddleLeft.png'))
blinkUpLeft = pygame.image.load(os.path.join(thisFolder, 'images\\player\\blinkupLeft.png'))
blinkDownMiddle = pygame.image.load(os.path.join(thisFolder, 'images\\player\\blinkcenterDown.png'))
blinkUpMiddle = pygame.image.load(os.path.join(thisFolder, 'images\\player\\blinkcenterUp.png'))

#Sets initial player (X, Y) values
playerX = 100
playerY = 480
#Creates the player object at the initial values
Player = player(screen, playerX, playerY, playerImg.get_size()[0], playerImg.get_size()[1])
#Initializes how much the player is changing in each direction to 0, updated by game loop
playerChangeX = 0
playerChangeY = 0

#platforms
#tileSize is ideal size for a platform, the platforms should all be this size
tileSize = (50, 50)
tileSizes = {'player' : (50, 50), 'blocks' : (50, 50), 'particles' : (20, 20), 'propulsions' : (50, 50)}
#image loading for platforms
boxGoalImg = pygame.image.load(os.path.join(thisFolder, 'images\\platformImages\\goal\\keyboxStatic.png'))
boxWinImg = pygame.image.load(os.path.join(thisFolder, 'images\\platformImages\\goal\\keyboxActivated.png'))
boxFailImg = pygame.image.load(os.path.join(thisFolder, "images\\platformImages\\goal\\keyboxDeactivated.png"))
wallTopImg = pygame.image.load(os.path.join(thisFolder, 'images\\platformImages\\walls\\wallcapTop.png'))
wallBottomImg = pygame.image.load(os.path.join(thisFolder, 'images\\platformImages\\walls\\wallcapBottom.png'))
wallImg = pygame.image.load(os.path.join(thisFolder, 'images\\platformImages\\walls\\wall.png'))
wall3WayImg = pygame.image.load(os.path.join(thisFolder, 'images\\platformImages\\walls\\wall3wayinterior.png'))
wall4WayImg = pygame.image.load(os.path.join(thisFolder, 'images\\platformImages\\walls\\wallcap4way.png'))
rawWallImg = pygame.image.load(os.path.join(thisFolder, 'images\\platformImages\\walls\\Interior.png'))
wallDoorImg = pygame.image.load(os.path.join(thisFolder, "images\\platformImages\\walls\\InteriorCap.png"))
nextLevelImg = pygame.image.load(os.path.join(thisFolder, "images\\platformImages\\nextLevelArrow.png"))
tealImage = pygame.image.load(os.path.join(thisFolder, "images\\platformImages\\keyBox\\keyInactive.png"))
tealHeldImage = pygame.image.load(os.path.join(thisFolder, "images\\platformImages\\keyBox\\keyActive.png"))
#Setting up platforms that are typically one use per level
platformGoal = platform(screen, 600, 350, boxGoalImg.get_size()[0], boxGoalImg.get_size()[1])
platformTeal = platform(screen, 200, 200, 50, 50)
platformExit = platform(screen, 850, 325, 50, 50)
platformBounce = platform(screen, 450, 350, 50, 50)
platformTeal2 = platform(screen, 500, 500, 50, 50)
platformKey = platform(screen, 200, 600, 50, 50)

#Flags
#Flags for player blinking
#Direction:
#0 = center
#1 = up left - nw
#2 = middle left - w
#3 = down left - sw
#4 = up right - ne
#5 = middle right - e
#6 = down right - se
#7 - middle up - n
#8 - middle down - s
#isBlink = determines if player is blinking
#blinkFrames = counter to determine blink length
direction = 0
isBlink = False
blinkFrames = 0
#movement flags to see if the key is pressed
movingLeft = False
movingRight = False
movingUp = False
movingDown = False
#Flag to see if the h key is being pressed
isCarryTeal = False
#Flag for seeing if level is complete
exitVisible = False
#Flag for removing certain collidable platforms
openDoor = False
doorsOpen = False
#Flag for what level the player is on
#-1 is the title screen
level = -1
#Flag for debug options
debugSetting = False
#Flags for bounce box
isBounce = False
noBounceTime = 0
#flag for what propulsion gear is being worn
propulsion = "fireExtinguisher"
#Flag for fading of particles
propulsionFade = 0
#Flag for testing to skip levels
levelSkip = False
#Flag for keycard collisions
keycardSuccess = False

#THESE ARE TEMP METHODS UNTIL I CAN FIGURE OUT SOMETHING BETTER
#OR MAYBE NOT TEMP DEPENDING ON HOW THIS GOES

#tutorial levels have no walls so no method needed

#builds walls for first level
def updateCollidable0():
    collidablePlatformsUpdate = []
    collidablePlatformsHitboxUpdate = []
    for iFunc in range(-50, pygame.display.get_surface().get_size()[0]+50, tileSizes.get("blocks", (50, 50))[0]):
        tempPlatform = platform(screen, iFunc, 100, tileSizes.get("blocks", (50, 50))[0], tileSizes.get("blocks", (50, 50))[1])
        collidablePlatformsUpdate.append(tempPlatform)
        tempPlatform = platform(screen, iFunc, 550, tileSizes.get("blocks", (50, 50))[0], tileSizes.get("blocks", (50, 50))[1])
        collidablePlatformsUpdate.append(tempPlatform)
    for jFunc in range(100, 550, 50):
        tempPlatform = platform(screen, 450, jFunc, 50, 50)
        collidablePlatformsUpdate.append(tempPlatform)
    for kFunc in range(0, len(collidablePlatformsUpdate)):
        collidablePlatformsHitboxUpdate.append(collidablePlatformsUpdate[kFunc].hitbox)
    return collidablePlatformsUpdate, collidablePlatformsHitboxUpdate

#builds walls for second level
def updateCollidable1():
    collidablePlatformsUpdate = []
    collidablePlatformsHitboxUpdate = []
    for iFunc in range(-50, pygame.display.get_surface().get_size()[0]+50, tileSizes.get("blocks", (50, 50))[0]):
        tempPlatform = platform(screen, 100, iFunc, tileSizes.get("blocks", (50, 50))[0], tileSizes.get("blocks", (50, 50))[1])
        collidablePlatformsUpdate.append(tempPlatform)
        tempPlatform = platform(screen, 800, iFunc, tileSizes.get("blocks", (50, 50))[0], tileSizes.get("blocks", (50, 50))[1])
        collidablePlatformsUpdate.append(tempPlatform)
    for kFunc in range(0, len(collidablePlatformsUpdate)):
        collidablePlatformsHitboxUpdate.append(collidablePlatformsUpdate[kFunc].hitbox)
    return collidablePlatformsUpdate, collidablePlatformsHitboxUpdate

#builds walls for third level
def updateCollidable2():
    collidablePlatformsUpdate = []
    collidablePlatformsHitboxUpdate = []
    for iFunc in range(-50, pygame.display.get_surface().get_size()[0]+50, tileSizes.get("blocks", (50, 50))[0]):
        tempPlatform = platform(screen, iFunc, 0, tileSizes.get("blocks", (50, 50))[0], tileSizes.get("blocks", (50, 50))[1])
        collidablePlatformsUpdate.append(tempPlatform)
        tempPlatform = platform(screen, iFunc, 650, tileSizes.get("blocks", (50, 50))[0], tileSizes.get("blocks", (50, 50))[1])
        collidablePlatformsUpdate.append(tempPlatform)
    for jFunc in range(50, 650, 50):
        tempPlatform = platform(screen, 450, jFunc, 50, 50)
        collidablePlatformsUpdate.append(tempPlatform)
    for kFunc in range(0, len(collidablePlatformsUpdate)):
        collidablePlatformsHitboxUpdate.append(collidablePlatformsUpdate[kFunc].hitbox)
    return collidablePlatformsUpdate, collidablePlatformsHitboxUpdate

#END (potentially) TEMP METHODS

#Some not so temp methods:
#https://nerdparadise.com/programming/pygameblitopacity
def blitAlpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface(tileSizes.get('particles')).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)

def abruptStopMusic():
    for iFunc in range(0, 5, 1):
        if pygame.mixer.Channel(iFunc+1).get_volume() > 0:
            pygame.mixer.Channel(iFunc+1).set_volume(0)

def goalBox(character, box, goalBoxDefault, goalBoxSuccess, goalBoxFailure, flag):
    #if the player collides with the goal without completing the objective, displays a fail image
    if character.rectCollide(box.hitbox) and not flag:
        box.draw(image = goalBoxFailure)
    #if the player collides with the box while completing the objective, displays a success image
    elif flag:
        box.draw(image = goalBoxSuccess)
    #draws standard goal image
    else:
        box.draw(image = goalBoxDefault)

#def keyBox(character, box1, box2, default, success, failure):
    #if character.rectCollide(box2) and not keycardSuccess:
    #    box1.draw(image = failure)
    #elif keycardSuccess:
    #    box1.draw(image = success)
    #else:
    #    box1.draw(image = default)
    #return box1.rectCollide(box2)
    

def carryBox(character, box, carrying, carryBoxDefault = None, carryBoxCarry = None):
    #if pressing h and touching the object, you can pick it up and move it
    if character.rectCollide(box.hitbox) and carrying:
        box.update(playerChangeX, playerChangeY, platformTeal.width, platformTeal.height)
        if carryBoxCarry is None:
            box.draw(color = YELLOW)
        else:
            box.draw(image = carryBoxCarry)
    #Draws it yellow even if not pressing h
    elif Player.rectCollide(box.hitbox) and not carrying:
        if carryBoxCarry is None:
            box.draw(color = YELLOW)
        else:
            box.draw(image = carryBoxCarry)
    #Draws the box when not being touched/moved
    else:
        carrying = False
        if carryBoxDefault is None:
            box.draw(color = TEAL)
        else:
            box.draw(image = carryBoxDefault)
    return carrying

def goalAccomplish(box1, box2):
    #if movable touches goal, draws the exit
    if box1.rectCollide(box2.hitbox):
        box2.draw(image = boxWinImg)
        return True
    return False

def bounceBox(character, box, flag, bounceTimer, tile, VelocityX, VelocityY, image = None):
    #creates a bounce box that bounces you away
    #REALLY buggy, let's just not worry about it for now
    #Known bugs:
    #   - if you change directions right as you collide, you get stuck in the box (near 0 velocities get you stuck, basically)
    #   - sometimes it doesn't contract despite colliding
    #This doesn't work at all so will probably scrap it - can't think of a use anyway
    vX = VelocityX
    vY = VelocityY

    if character.rectCollide(box.hitbox) and not flag:
        box.updateCardinal(box.origin[0]+5, box.origin[1]+5, tile[0]-10, tile[1]-10)
        if vX < 0 and vY < 0:
            character.updateCardinal(box.origin[0]+10, box.origin[1]+10, character.width, character.height)
        if vX > 0 and vY > 0:
            character.updateCardinal(box.origin[0]-10, box.origin[1]-10, character.width, character.height)
        if vX < 0 and vY > 0:
            character.updateCardinal(box.origin[0]+10, box.origin[1]-10, character.width, character.height)
        if vX > 0 and vY < 0:
            character.updateCardinal(box.origin[0]-10, box.origin[1]+10, character.width, character.height)
        if vX < 0 and vY == 0:
            character.updateCardinal(box.origin[0]+10, character.top, character.width, character.height)
        if vX > 0 and vY == 0:
            character.updateCardinal(box.origin[0]-10, character.top, character.width, character.height)
        if vX == 0 and vY < 0:
            character.updateCardinal(character.left, box.origin[1]-10, character.width, character.height)
        if vX == 0 and vY > 0:
            character.updateCardinal(character.left, box.origin[1]+10, character.width, character.height)
        if vX == 0 and vY == 0:
            character.updateCardinal(character.left-30, character.top-30, character.width, character.height)
        vX = -vX
        vY = -vY
        character.accelX = -character.accelX
        character.accelY = -character.accelY
        flag = True
        if not pygame.mixer.Channel(23).get_busy():
            pygame.mixer.Channel(23).set_volume(0.4)
            pygame.mixer.Channel(23).play(springSound)
        box.draw(color = BLUE)
    elif character.rectCollide(box.hitbox) and flag:
        bounceTimer += 1
        if bounceTimer > 1:
            bounceTimer = 0
            flag = False
        box.draw(color = BLUE)
    else:
        box.updateCardinal(platformBounce.origin[0], platformBounce.origin[1], tileSizes.get("blocks", (50, 50))[0], tileSizes.get("blocks", (50, 50))[0])
        box.draw(color = BLUE)
    return vX, vY, flag, bounceTimer

#Makes the lists to be updated to be drawn later
collidablePlatforms = []
collidablePlatformsHitboxes = []
#Loads "You Win! :)" image and centers it
winBanner = pygame.image.load(os.path.join(thisFolder, "images\\misc\\youWin.png"))
winRect = pygame.Rect(center, (winBanner.get_size()[0], winBanner.get_size()[1]))
winRect.center = center

propulsionSounds = []

#propulsion gear image loading
if propulsion == "fireExtinguisher":
    propulsionImgLeft = pygame.image.load(os.path.join(thisFolder, 'images\\extinguisher\\extinguisherLeft.png'))
    propulsionImgRight = pygame.image.load(os.path.join(thisFolder, 'images\\extinguisher\\extinguisherRight.png'))
    propulsionParticles = pygame.image.load(os.path.join(thisFolder, 'images\\extinguisher\\extinguisherParticles.png'))
    for j in range(1, 16, 1):
        soundTemp = pygame.mixer.Sound(os.path.join(thisFolder, "sounds\\fireExtinguisher\\extng"+str(j)+".wav"))
        propulsionSounds.append(soundTemp)
pygame.mixer.Channel(22).set_volume(0.3)
#Initial rectangle for propulsion gear, quickly overwritten later
propulsionRect = pygame.Rect(0,0,0,0)
propulsionParticleRect = pygame.Rect(0, 0, 0, 0)

#Setting the maximums so as to not break the game and make it more fluid
maxSpeedX = 10
maxSpeedY = 10
maxVelX = 80
maxVelY = 80
maxFrictionX = 10
maxFrictionY = 10
maxSpeed = math.sqrt(math.pow(maxVelX, 2) + math.pow(maxVelY, 2))

#Loads the image for the background
backgroundImg = pygame.image.load(os.path.join(thisFolder, "images\\spaceBG.png")).convert()

#starts timer to count frames and time
timer = 0
#increments time
dT = 1/FPS * 10

#sets initial velocity and friction values, updated upon movement
velocityX = 0
velocityY = 0
frictionX = 0
frictionY = 0

#Loop to keep screen running until exit is clicked
running = True
while running:

    #Sets background in RGB
    #screen.fill(SPACE_PURPLE)

    #Fills in the bottom layer with a background image
    screen.blit(backgroundImg, [0,0])
    
    #If moving, increases friction until it hits cap
    #if velocity is 0 (or basically 0), sets friction to 0
    if abs(velocityX) > 1:
        frictionX = 10 * (math.pow(velocityX, 2) * Player.friction * (velocityX/abs(velocityX)))
        if frictionX > maxFrictionX:
            frictionX = maxFrictionX
        if frictionX < -maxFrictionX:
            frictionX = -maxFrictionX
    else:
        frictionX = 0
    if abs(velocityY) > 1:
        frictionY = 10 * (math.pow(velocityY, 2) * Player.friction * (velocityY/abs(velocityY)))
        if frictionY > maxFrictionY:
            frictionY = maxFrictionY
        if frictionY < -maxFrictionY:
            frictionY = -maxFrictionY
    else:
        frictionY = 0

    #determines how fast a player will go based on real physics equations - thank you AND screw you, Matt
    playerChangeX = ((Player.accelX + frictionX) * 0.5 * math.pow(dT, 2)) + (velocityX * dT)
    playerChangeY = ((Player.accelY + frictionY) * 0.5 * math.pow(dT, 2)) + (velocityY * dT)

    #Checks for events every frame to do things
    for event in pygame.event.get():

        #Checks for user trying to quit
        if event.type == pygame.QUIT:
            running = False

        #Checks for useful keystrokes
        #WASD for movement
        if event.type == pygame.KEYDOWN:
            #print(event.key)
            if event.key == pygame.K_a:
                movingLeft = True
                Player.accelX += -1
            if event.key == pygame.K_d:
                movingRight = True
                Player.accelX += 1
            if event.key == pygame.K_s:
                movingDown = True
                Player.accelY += 1
            if event.key == pygame.K_w:
                movingUp = True
                Player.accelY += -1
            #uses right enter key for picking up the pick-up-able item
            if event.key == 13 and not isCarryTeal:
                isCarryTeal = True
                isCarryTeal2 = True
            if event.key == pygame.K_l:
                levelSkip = True
                

        #Checks for release of keys
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                movingLeft = False
            if event.key == pygame.K_d:
                movingRight = False
            if event.key == pygame.K_s:
                movingDown = False
            if event.key == pygame.K_w:
                movingUp = False
            #poorly documented event types, 13 is right enter
            if event.key == 13:
                isCarryTeal = False
            if event.key == pygame.K_l:
                levelSkip = False

    #When holding a key, move faster each frame in that direction
    if movingLeft:
        Player.accelX += -0.05
        if abs(Player.accelX) > maxSpeedX:
            Player.accelX = -maxSpeedX
        velocityX += (Player.accelX * dT)
        if velocityX < -maxVelX:
            velocityX = -maxVelX
    if movingRight:
        Player.accelX += 0.05
        if abs(Player.accelX) > maxSpeedX:
            Player.accelX = maxSpeedX
        velocityX += (Player.accelX * dT)
        if velocityX > maxVelX:
            velocityX = maxVelX
    if movingUp:
        Player.accelY += -0.05
        if abs(Player.accelY) > maxSpeedY:
            Player.accelY = -maxSpeedY
        velocityY += (Player.accelY * dT)
        if velocityY < -maxVelY:
            velocityY = -maxVelY
    if movingDown:
        Player.accelY += 0.05
        if abs(Player.accelY) > maxSpeedY:
            Player.accelY = maxSpeedY
        velocityY += (Player.accelY * dT)
        if velocityY > maxVelY:
            velocityY = maxVelY

    #When not pressing button
    if Player.accelX < 0 and not movingLeft:
        Player.accelX += 0.1
        if Player.accelX < 1.1 and Player.accelX > -1.1:
            Player.accelX = 0
        velocityX -= (Player.accelX * dT)
        if velocityX > -2:
            velocityX = 0
    if Player.accelX > 0 and not movingRight:
        Player.accelX += -0.1
        if Player.accelX > -1.1 and Player.accelX < 1.1:
            Player.accelX = 0
        velocityX -= (Player.accelX * dT)
        if velocityX < 2:
            velocityX = 0
    if Player.accelY < 0 and not movingUp:
        Player.accelY += 0.1
        if Player.accelY < 1.1 and Player.accelY > -1.1:
            Player.accelY = 0
        velocityY -= (Player.accelY * dT)
        if velocityY > -2:
            velocityY = 0
    if Player.accelY > 0 and not movingDown:
        Player.accelY += -0.1
        if Player.accelY > -1.1 and Player.accelY < 1.1:
            Player.accelY = 0
        velocityY -= (Player.accelY * dT)
        if velocityY < 2:
            velocityY = 0

    #Handles if acceleration is 0
    if Player.accelX == 0:
        if velocityX > 1.1:
            velocityX -= 0.2
        elif velocityX < -1.1:
            velocityX += 0.2
        else:
            velocityX = 0
    if Player.accelY == 0:
        if velocityY > 1.1:
            velocityY -= 0.2
        elif velocityY < -1.1:
            velocityY += 0.2
        else:
            velocityY = 0

    #Behold: the BLINK engine!
    #all this shit determines what to do if you're not blinking...
    if not isBlink:
        if movingDown and movingLeft and movingRight and movingUp:
            playerImg = lookCenter
            direction = 0
        elif (movingDown and not movingUp and not movingLeft and not movingRight) or (movingDown and movingLeft and movingRight):
            playerImg = downMiddle
            direction = 8
        elif (movingUp and movingLeft and movingRight) or (movingUp and not movingDown and not movingLeft and not movingRight):
            playerImg = upMiddle
            direction = 7
        elif (movingLeft and not movingUp and not movingDown and not movingRight) or (movingUp and movingDown and movingLeft):
            playerImg = middleLeft
            direction = 2
        elif (movingRight and not movingUp and not movingLeft and not movingDown) or (movingUp and movingDown and movingRight):
            playerImg = middleRight
            direction = 5
        elif movingDown and movingRight:
            playerImg = downRight
            direction = 6
        elif movingUp and movingRight:
            playerImg = upRight
            direction = 4
        elif movingDown and movingLeft:
            playerImg = downLeft
            direction = 3
        elif movingUp and movingLeft:
            playerImg = upLeft
            direction = 1
        else:
            playerImg = lookCenter
            direction = 0
    #...and this says what should happen if you are blinking which is determined by...
    else:
        blinkFrames += 1
        if blinkFrames > 8:
            isBlink = False
            blinkFrames = 0

    #...this, which gives you a 1/420 chance if the random number is 69 to blink and then loads
    #the image based on the information above and how many frames have passed.
    if random.randrange(420-420, 420+1, 1) == 69 and not isBlink:
        isBlink = True
        if direction == 0:
            playerImg = blinkCenter
        if direction == 1:
            playerImg = blinkUpLeft
        if direction == 2:
            playerImg = blinkMiddleLeft
        if direction == 3:
            playerImg = blinkDownLeft
        if direction == 4:
            playerImg = blinkUpRight
        if direction == 5:
            playerImg = blinkMiddleRight
        if direction == 6:
            playerImg = blinkDownRight
        if direction == 7:
            playerImg = blinkUpMiddle
        if direction == 8:
            playerImg = blinkDownMiddle

    #updating player position 
    playerX += playerChangeX
    playerY += playerChangeY


    #Adding screen boundaries
    #Currently - Pac-Man style, go in one side, come out the other
    if playerX <= -50:
        playerX = 950
    elif playerX >= 950:
        playerX = -50

    if playerY <= -50:
        playerY = 750
    elif playerY >= 750:
        playerY = -50

    #Determining total speed of player
    #A man has fallen into the river at this speed in Velo City!
    #HEY!
    speed = math.sqrt(math.pow(velocityX, 2) + math.pow(velocityY, 2))
    proportionalSpeed = speed/maxSpeed 

    if Player.hitbox.collidelistall(collidablePlatformsHitboxes):
    #    print (Player.hitbox.collidelistall(collidablePlatformsHitboxes))
    #    pygame.draw.rect(screen, YELLOW, Player.hitbox)
        pass

    #if the player is not colliding with a platform, do nothing
    if Player.hitbox.collidelist(collidablePlatformsHitboxes) == -1:
        pass

    #if the player is colliding with a platform
    if not Player.hitbox.collidelist(collidablePlatformsHitboxes) == -1:
        #Tells which box is being collided with (uses first if multiple)
        collidedIndex = Player.hitbox.collidelist(collidablePlatformsHitboxes)
        #print(collidedIndex)
        colPlats = [collidablePlatformsHitboxes[collidedIndex]]
        #print(Player.hitbox.collidelist(collidablePlatformsHitboxes))

        #if False:
        for colPlat in Player.hitbox.collidelistall(collidablePlatformsHitboxes):
            #detects top of player and bottom of platform
            if Player.hitbox.top < collidablePlatformsHitboxes[colPlat].bottom and Player.hitbox.top > collidablePlatformsHitboxes[colPlat].top and velocityY < 0:
                #print("here1")
                Player.accelY = 0
                velocityY = 0
                playerY = Player.hitbox.top
                #print("bottom of " + str(collidablePlatformsHitboxes.index(collidablePlatformsHitboxes[colPlat])))

            elif Player.hitbox.bottom > collidablePlatformsHitboxes[colPlat].top and Player.hitbox.bottom < collidablePlatformsHitboxes[colPlat].bottom and velocityY > 0:
                #print("here2")
                Player.accelY = 0
                velocityY = 0
                playerY = Player.hitbox.top
                #print("top of " + str(collidablePlatformsHitboxes.index(collidablePlatformsHitboxes[colPlat])))
            
            elif Player.hitbox.right > collidablePlatformsHitboxes[colPlat].left and Player.hitbox.right < collidablePlatformsHitboxes[colPlat].right and velocityX > 0:
                #print("here3")
                Player.accelX = 0
                velocityX = 0
                playerX = Player.hitbox.left
                #print("left of " + str(collidablePlatformsHitboxes.index(collidablePlatformsHitboxes[colPlat])))

            elif Player.hitbox.left < collidablePlatformsHitboxes[colPlat].right and Player.hitbox.left > collidablePlatformsHitboxes[colPlat].left and velocityX < 0:
                #print("here4")
                Player.accelX = 0
                velocityX = 0
                playerX = Player.hitbox.left
                #print("right of " + str(collidablePlatformsHitboxes.index(collidablePlatformsHitboxes[colPlat])))
            

    """
    #ANTIQUATED MOVEMENT ENGINE

    #more elegant now but still pretty ugly
    #dynamic boxes and collision areas for all platforms listed in "collidablePlatforms"
    for plat in collidablePlatforms:
            
            hitWallLeft = Player.hitbox.right <= plat.hitbox.left+5 and Player.hitbox.left < plat.hitbox.left+5 and velocityX >= 0
            hitWallRight = Player.hitbox.left >= plat.hitbox.right-5 and Player.hitbox.right > plat.hitbox.right-5 and velocityX <= 0
            hitWallBottom = Player.hitbox.top >= plat.hitbox.bottom-5 and Player.hitbox.bottom > plat.hitbox.bottom-5 and velocityY <= 0
            hitWallTop = Player.hitbox.bottom <= plat.hitbox.top+5 and Player.hitbox.top < plat.hitbox.top+5 and velocityY >= 0

            if hitWallLeft and hitWallBottom and not hitWallTop and not hitWallRight:
                #print("right+up")
                pass

            elif hitWallLeft and hitWallTop and not hitWallBottom and not hitWallRight:
                #print("right+down")
                pass

            elif hitWallRight and hitWallBottom and not hitWallTop and not hitWallLeft:
                #print("left+up")
                pass

            elif hitWallRight and hitWallTop and not hitWallBottom and not hitWallLeft:
                #print("left+down")
                pass

            #moving right
            elif hitWallLeft and not hitWallRight and not hitWallTop and not hitWallBottom:
                #print("right")
                Player.accelX = 0
                velocityX = 0
                playerX = Player.hitbox.left
            
            #moving left
            elif hitWallRight and not hitWallLeft and not hitWallTop and not hitWallBottom:
                #print("left")
                Player.accelX = 0
                velocityX = 0
                playerX = Player.hitbox.left

            #moving up
            elif hitWallBottom and not hitWallLeft and not hitWallRight and not hitWallTop:
                #print("up")
                Player.accelY = 0
                velocityY = 0
                playerY = Player.hitbox.top

            #moving down
            elif hitWallTop and not hitWallLeft and not hitWallRight and not hitWallBottom:
                #print("down")
                Player.accelY = 0
                velocityY = 0
                playerY = Player.hitbox.top

            #y = 100 if player.top > 105 player.top = 100

    #"""

    #BEGIN BACKGROUND MUSIC MANAGEMENT

    #at the start of the game, starts all music at appropriate volume and loops them forever
    if not pygame.mixer.Channel(0).get_busy():
        pygame.mixer.Channel(0).set_volume(0.2)
        pygame.mixer.Channel(0).play(backgroundSounds[0], loops = -1, fade_ms = 1000)
    if not pygame.mixer.Channel(1).get_busy():
        pygame.mixer.Channel(1).set_volume(0.0)
        pygame.mixer.Channel(1).play(backgroundSounds[1], loops = -1)
    if not pygame.mixer.Channel(2).get_busy():
        pygame.mixer.Channel(2).set_volume(0.0)
        pygame.mixer.Channel(2).play(backgroundSounds[2], loops = -1)
    if not pygame.mixer.Channel(3).get_busy():
        pygame.mixer.Channel(3).set_volume(0.0)
        pygame.mixer.Channel(3).play(backgroundSounds[3], loops = -1)
    if not pygame.mixer.Channel(4).get_busy():
        pygame.mixer.Channel(4).set_volume(0.0)
        pygame.mixer.Channel(4).play(backgroundSounds[4], loops = -1)
    if not pygame.mixer.Channel(5).get_busy():
        pygame.mixer.Channel(5).set_volume(0.0)
        pygame.mixer.Channel(5).play(backgroundSounds[5], loops = -1)
    if not pygame.mixer.Channel(6).get_busy():
        pygame.mixer.Channel(6).set_volume(0.0)
        pygame.mixer.Channel(6).play(backgroundSounds[6], loops = -1)
    if not pygame.mixer.Channel(7).get_busy():
        pygame.mixer.Channel(7).set_volume(0.0)
        pygame.mixer.Channel(7).play(backgroundSounds[7], loops = -1)

    #Certain tracks play only if the player's speed is a certain value and then plays
    #the track at the proportional volume to the (max speed - arbitrarySpeed) so it doesn't
    #destroy my eardrums every time I test it
    #print(proportionalSpeed)
    if proportionalSpeed >= 0.2:
        if proportionalSpeed - 0.2 > 0.3:
            pygame.mixer.Channel(1).set_volume(0.3)
        else:
            pygame.mixer.Channel(1).set_volume(proportionalSpeed - 0.2)
    if proportionalSpeed >= 0.3:
        if proportionalSpeed - 0.4 > 0.3:
            pygame.mixer.Channel(2).set_volume(0.3)
        else:
            pygame.mixer.Channel(2).set_volume(proportionalSpeed - 0.4)
    if proportionalSpeed >= 0.3:
        if proportionalSpeed - 0.6 > 0.3:
            pygame.mixer.Channel(3).set_volume(0.3)
        else:
            pygame.mixer.Channel(3).set_volume(proportionalSpeed - 0.6)
    if proportionalSpeed >= 0.8:
        if proportionalSpeed - 0.8 > 0.3:
            pygame.mixer.Channel(4).set_volume(0.3)
        else:
            pygame.mixer.Channel(4).set_volume(proportionalSpeed - 0.8)
    if proportionalSpeed >= 0.9:
        pygame.mixer.Channel(5).set_volume(proportionalSpeed - 0.9)


    #END BACKGROUND MUSIC MANAGEMENT

    #tutorial screen 1
    if level == -1:
        #setting up images and drawings for the title and instructions
        screen.blit(titleImg, titleImg.get_rect())
        instructionsRect = pygame.Rect(400, 0, 300, 300)
        screen.blit(instructionsImg, instructionsRect)
        platformExit.draw(image = nextLevelImg)
        instructionsRect2 = pygame.Rect(600, 400, 300, 300)
        screen.blit(instructionsImg2, instructionsRect2)
        
        #Going to the next level is always unique, and so this won't be put into a function
        #checks if the player is touching the way to leave, then sets up for the next level appropriately
        if Player.rectCollide(platformExit.hitbox) or levelSkip:
            levelSkip = False
            #Stops music abruptly for level transition
            abruptStopMusic()
            #Changes level
            level = -2
            #Spawns player here in new level
            playerX = 300
            playerY = 450
            #Reset all speed factors so they aren't moving when new level starts
            Player.accelX = 0
            Player.accelY = 0
            velocityX = 0
            velocityY = 0
            #updates various platforms to new positions
            platformGoal.updateCardinal(725, 425, 50, 50)
            platformTeal.updateCardinal(100, 250, 50, 50)

    #tutorial screen 2
    if level == -2:
        #Drawing instructions and the necessary boxes
        screen.blit(insructionsTeal, insructionsTeal.get_rect())
        instructionsGoalRect = pygame.Rect(600, 350, 300, 300)
        screen.blit(instructionsGoal, instructionsGoalRect)

        goalBox(Player, platformGoal, boxGoalImg, boxWinImg, boxFailImg, exitVisible)

        isCarryTeal = carryBox(Player, platformTeal, isCarryTeal, carryBoxDefault = tealImage, carryBoxCarry = tealHeldImage)
    
        exitVisible = goalAccomplish(platformTeal, platformGoal)
        #if exitVisible:
            #screen.blit(winBanner, winRect)

        #lets player move on to next level
        if Player.rectCollide(platformExit.hitbox) and exitVisible or levelSkip:
            levelSkip = False
            abruptStopMusic()
            playerX = 300
            playerY = 450
            platformGoal.updateCardinal(600, 350, platformGoal.width, platformGoal.height)
            platformTeal.updateCardinal(500, 200, platformTeal.width, platformTeal.height)
            exitVisible = False
            collidablePlatforms, collidablePlatformsHitboxes = updateCollidable0()
            Player.accelX = 0
            Player.accelY = 0
            velocityX = 0
            velocityY = 0
            level = 0
            #pygame.time.wait(1000)
        elif exitVisible:
            platformExit.draw(image = nextLevelImg)

    #Level 1
    if level == 0:
        goalBox(Player, platformGoal, boxGoalImg, boxWinImg, boxFailImg, exitVisible)

        isCarryTeal = carryBox(Player, platformTeal, isCarryTeal, carryBoxDefault = tealImage, carryBoxCarry = tealHeldImage)

        for plat in collidablePlatforms:
            if plat.left == 0 and plat.top == 550:
                plat.draw(orientation = 3, image = wallTopImg)
            elif plat.left == 850 and plat.top == 550:
                plat.draw(orientation = 3, image = wallBottomImg)
            elif plat.left == 0 and plat.top == 100:
                plat.draw(orientation = 1, image = wallBottomImg)
            elif plat.left == 850 and plat.top == 100:
                plat.draw(orientation = 1, image = wallTopImg)
            elif plat.top == 100 and plat.left == 450:
                plat.draw(orientation = 0, image = wall3WayImg)
            elif plat.top == 550 and plat.left == 450:
                plat.draw(orientation = 2, image = wall3WayImg)
            elif plat.top == 100:
                plat.draw(orientation = 1, image = wallImg)
            elif plat.top == 550:
                plat.draw(orientation = 3, image = wallImg)
            else:
                plat.draw(image = rawWallImg)
            #pygame.draw.rect(screen, GREEN, plat.hitbox, 3)

        exitVisible = goalAccomplish(platformTeal, platformGoal)

        if Player.rectCollide(platformExit.hitbox) and exitVisible or levelSkip:
            levelSkip = False
            abruptStopMusic()
            playerX = 300
            playerY = 450
            platformTeal.updateCardinal(400, 600, platformTeal.width, platformTeal.height)
            exitVisible = False
            collidablePlatforms, collidablePlatformsHitboxes = updateCollidable1()
            Player.accelX = 0
            Player.accelY = 0
            velocityX = 0
            velocityY = 0
            level = 1
            #pygame.time.wait(1000)
        elif exitVisible:
            platformExit.draw(image = nextLevelImg)
    
    #Level 2
    if level == 1:
        #print("level 1")
        goalBox(Player, platformGoal, boxGoalImg, boxWinImg, boxFailImg, exitVisible)
        goalBox(Player, platformKey, boxGoalImg, boxWinImg, boxFailImg, keycardSuccess)

        isCarryTeal = carryBox(Player, platformTeal, isCarryTeal, carryBoxDefault = tealImage, carryBoxCarry = tealHeldImage)

        for plat in collidablePlatforms:
            if plat.top == 0:
                if plat.left == 100:
                    plat.draw(orientation = 0, image = wallTopImg)
                else:
                    plat.draw(orientation = 2, image = wallBottomImg)
            elif plat.top == 650:
                if plat.left == 800:
                    plat.draw(orientation = 2, image = wallTopImg)
                else:
                    plat.draw(orientation = 0, image = wallBottomImg)
            elif plat.left == 100:
                plat.draw(orientation = 0, image = wallImg)
            elif plat.left == 800 and plat.top == 250:
                plat.draw(orientation = 2, image = wallTopImg)
            elif plat.left == 800 and plat.top == 400:
                plat.draw(orientation = 2, image = wallBottomImg)
            else:
                plat.draw(orientation = 2, image = wallImg)


        exitVisible = goalAccomplish(platformTeal, platformGoal)
        keycardSuccess = goalAccomplish(platformTeal, platformKey)

        if keycardSuccess:
            openDoor = True
        else:
            openDoor = False
        #levelSkip = True
        if Player.rectCollide(platformExit.hitbox) and exitVisible or levelSkip:
            levelSkip = False
            abruptStopMusic()
            collidablePlatforms, collidablePlatformsHitboxes = updateCollidable2()
            playerX = 200
            playerY = 450
            exitVisible = False
            keycardSuccess = False
            openDoor = False
            doorsOpen = False
            Player.accelX = 0
            Player.accelY = 0
            velocityX = 0
            velocityY = 0
            level = 2
            platformKey.updateCardinal(400, 400, platformKey.width, platformKey.height)
            platformTeal.updateCardinal(200, 300, platformTeal.width, platformTeal.height)
            platformGoal.updateCardinal(700, 300, platformGoal.width, platformGoal.height)
        elif exitVisible:
            platformExit.draw(image = nextLevelImg)

        #opens wall to move on
        #Add door "whoosh" or keycard beeps to show success
        if openDoor and not doorsOpen:
                for index, item in enumerate(collidablePlatforms):
                    if (item.hitbox.left == 800 and item.hitbox.top == 350) or (item.hitbox.left == 800 and item.hitbox.top == 300):
                        item.updateCardinal(-50, -50, 0, 0)
                for index, item in enumerate(collidablePlatformsHitboxes):
                    if (item.left == 800 and item.top == 350) or (item.left == 800 and item.top == 300):
                        collidablePlatformsHitboxes.remove(item)
                pygame.mixer.Channel(21).play(doorSound)
                doorsOpen = True
                openDoor = False

    #level 3
    if level == 2:

        goalBox(Player, platformGoal, boxGoalImg, boxWinImg, boxFailImg, exitVisible)
        goalBox(Player, platformKey, boxGoalImg, boxWinImg, boxFailImg, keycardSuccess)

        isCarryTeal = carryBox(Player, platformTeal, isCarryTeal, carryBoxDefault = tealImage, carryBoxCarry = tealHeldImage)

        for plat in collidablePlatforms:
            if plat.left == 0 and plat.top == 0:
                plat.draw(orientation = 1, image = wallBottomImg)
            elif plat.left == 850 and plat.top == 0:
                plat.draw(orientation = 1, image = wallTopImg)
            elif plat.left == 0 and plat.top == 650:
                plat.draw(orientation = 3, image = wallTopImg)
            elif plat.left == 850 and plat.top == 650:
                plat.draw(orientation = 3, image = wallBottomImg)
            elif plat.top == 0 and plat.left == 450:
                plat.draw(orientation = 0, image = wall3WayImg)
            elif plat.top == 650 and plat.left == 450:
                plat.draw(orientation = 2, image = wall3WayImg)
            elif plat.top == 400:
                plat.draw(orientation = 0, image = wallDoorImg)
            elif plat.top == 250:
                plat.draw(orientation = 2, image = wallDoorImg)
            elif plat.top == 0:
                plat.draw(orientation = 1, image = wallImg)
            elif plat.top == 650:
                plat.draw(orientation = 3, image = wallImg)
            else:
                plat.draw(image = rawWallImg)

        exitVisible = goalAccomplish(platformTeal, platformGoal)
        keycardSuccess = goalAccomplish(platformTeal, platformKey)

        if keycardSuccess:
            openDoor = True
        else:
            openDoor = False

        if Player.rectCollide(platformExit.hitbox) and exitVisible or levelSkip:
            levelSkip = False
            abruptStopMusic()
            collidablePlatforms = []
            playerX = 200
            playerY = 450
            exitVisible = False
            openDoor = False
            doorsOpen = False
            level = 3
            Player.accelX = 0
            Player.accelY = 0
            velocityX = 0
            velocityY = 0
            platformTeal.updateCardinal(850, 650, platformTeal.width, platformTeal.height)
            platformGoal.updateCardinal(850, 0, platformGoal.width, platformGoal.height)
        
        elif exitVisible:
            platformExit.draw(image = nextLevelImg)
            
        if openDoor and not doorsOpen:
            for index, item in enumerate(collidablePlatforms):
                if (item.hitbox.left == 450 and item.hitbox.top == 350) or (item.hitbox.left == 450 and item.hitbox.top == 300):
                    item.updateCardinal(-50, -50, 0, 0)
            #for index, item in enumerate(collidablePlatformsHitboxes):
            #    if (item.left == 450 and item.top == 350) or (item.left == 450 and item.top == 300):
            #        print("here")
            #        print(item)
            #        print(item in collidablePlatformsHitboxes)
            #        collidablePlatformsHitboxes.remove(item)
            #        print(item in collidablePlatformsHitboxes)
            #print("predel 45: "+ str(collidablePlatformsHitboxes[45]))
            #print("predel 46: "+ str(collidablePlatformsHitboxes[46]))
            del collidablePlatformsHitboxes[45]
            del collidablePlatformsHitboxes[45]
            #print("postdel 45: "+ str(collidablePlatformsHitboxes[45]))
            #print("postdel 46: "+ str(collidablePlatformsHitboxes[46]))
            doorsOpen = True
            openDoor = False
            pygame.mixer.Channel(21).play(doorSound)

    #sets a track to play if player is holding box
    if Player.rectCollide(platformTeal.hitbox) and isCarryTeal:
        pygame.mixer.Channel(6).set_volume(0.15)
    else:
        pygame.mixer.Channel(6).set_volume(0.00)

    #victory music - if goal is visible, play this
    if exitVisible:
        pygame.mixer.Channel(7).set_volume(0.15)
    else:
        pygame.mixer.Channel(7).set_volume(0.00)

    #Runs player and changes icon position accordingly
    Player.updateCardinal(playerX, playerY, Player.width, Player.height)
    Player.draw(playerImg)
    #pygame.draw.rect(screen, RED, Player.hitbox, 3)
    #HERE DIPSHIT

    propulsionSound = propulsionSounds[random.randrange(0, len(propulsionSounds))]

    #determines where the propulsion shit happens and stuff
    #I wish this wasn't so FUCKING cluttered but I think it needs to be, unfortunately
    #Maybe turn all this shit into functions just so it's easier to digest down here, anyway
    #arbitrary values are just to make it look nice.  Had to manually tweak all of them.
    #Will probably have to do a bajillion if statements (or make individual functions)
    #if/when adding new propulsion images
    if direction == 8:
        propulsionFade = 0
        blitAlpha(screen, pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), pygame.Rect(propulsionParticleRect.left, propulsionParticleRect.top-10, 20, 20), 128)
        pygame.mixer.Channel(22).play(propulsionSound)
        propulsionRect = pygame.Rect(Player.left, Player.top-20, 40, 40)
        propulsionParticleRect = pygame.Rect(propulsionRect.left+20, propulsionRect.top-20, propulsionParticles.get_size()[0], propulsionParticles.get_size()[1])
        screen.blit(pygame.transform.rotate(propulsionImgLeft, -90), propulsionRect)
        screen.blit(pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), propulsionParticleRect)

    elif direction == 7:
        propulsionFade = 0
        blitAlpha(screen, pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), pygame.Rect(propulsionParticleRect.left, propulsionParticleRect.top+10, 20, 20), 128)
        pygame.mixer.Channel(22).play(propulsionSound)
        propulsionRect = pygame.Rect(Player.left, Player.top+20, 40, 40)
        propulsionParticleRect = pygame.Rect(propulsionRect.left+20, propulsionRect.top+35, propulsionParticles.get_size()[0], propulsionParticles.get_size()[1])
        screen.blit(pygame.transform.rotate(propulsionImgRight, -90), propulsionRect)
        screen.blit(pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), propulsionParticleRect)

    elif direction == 6:
        propulsionFade = 0
        blitAlpha(screen, pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), pygame.Rect(propulsionParticleRect.left-8, propulsionParticleRect.top-8, 20, 20), 128)
        pygame.mixer.Channel(22).play(propulsionSound)
        propulsionRect = pygame.Rect(Player.left-20, Player.top-20, 40,  40)
        propulsionParticleRect = pygame.Rect(propulsionRect.left+5, propulsionRect.top-13, propulsionParticles.get_size()[0], propulsionParticles.get_size()[1])
        screen.blit(pygame.transform.rotate(propulsionImgLeft, -45), propulsionRect)
        screen.blit(pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), propulsionParticleRect)

    elif direction == 5:
        propulsionFade = 0
        blitAlpha(screen, pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), pygame.Rect(propulsionParticleRect.left-10, propulsionParticleRect.top, 20, 20), 128)
        pygame.mixer.Channel(22).play(propulsionSound)
        propulsionRect = pygame.Rect(Player.left-20, Player.top, 40,  40)
        propulsionParticleRect = pygame.Rect(propulsionRect.left-20, propulsionRect.top, propulsionParticles.get_size()[0], propulsionParticles.get_size()[1])
        screen.blit(propulsionImgLeft, propulsionRect)
        screen.blit(pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), propulsionParticleRect)

    elif direction == 4:
        propulsionFade = 0
        blitAlpha(screen, pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), pygame.Rect(propulsionParticleRect.left-7, propulsionParticleRect.top+3, 20, 20), 128)
        pygame.mixer.Channel(22).play(propulsionSound)
        propulsionRect = pygame.Rect(Player.left-20, Player.top+10, 40,  40)
        propulsionParticleRect = pygame.Rect(propulsionRect.left-15, propulsionRect.top+27, propulsionParticles.get_size()[0], propulsionParticles.get_size()[1])
        screen.blit(pygame.transform.rotate(propulsionImgLeft, 45), propulsionRect)
        screen.blit(pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), propulsionParticleRect)

    elif direction == 3:
        propulsionFade = 0
        blitAlpha(screen, pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), pygame.Rect(propulsionParticleRect.left+7, propulsionParticleRect.top-7, 20, 20), 128)
        pygame.mixer.Channel(22).play(propulsionSound)
        propulsionRect = pygame.Rect(Player.left+20, Player.top, 40, 40)
        propulsionParticleRect = pygame.Rect(propulsionRect.left+25, propulsionRect.top-15, propulsionParticles.get_size()[0], propulsionParticles.get_size()[1])
        screen.blit(pygame.transform.rotate(propulsionImgRight, 45), propulsionRect)
        screen.blit(pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), propulsionParticleRect)

    elif direction == 2:
        propulsionFade = 0
        blitAlpha(screen, pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), pygame.Rect(propulsionParticleRect.left+12, propulsionParticleRect.top-2, 20, 20), 128)
        pygame.mixer.Channel(22).play(propulsionSound)
        propulsionRect = pygame.Rect(Player.left+30, Player.top, 40,  40)
        propulsionParticleRect = pygame.Rect(propulsionRect.left+35, propulsionRect.top-5, propulsionParticles.get_size()[0], propulsionParticles.get_size()[1])
        screen.blit(propulsionImgRight, propulsionRect)
        screen.blit(pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), propulsionParticleRect)

    elif direction == 1:
        propulsionFade = 0
        blitAlpha(screen, pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), pygame.Rect(propulsionParticleRect.left+7, propulsionParticleRect.top+7, 20, 20), 128)
        pygame.mixer.Channel(22).play(propulsionSound)
        propulsionRect = pygame.Rect(Player.left+10, Player.top+10, 40, 40)
        propulsionParticleRect = pygame.Rect(propulsionRect.left+43, propulsionRect.top+33, propulsionParticles.get_size()[0], propulsionParticles.get_size()[1])
        screen.blit(pygame.transform.rotate(propulsionImgRight, -45), propulsionRect)
        screen.blit(pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), propulsionParticleRect)
    else:
        if propulsionFade < 10:
            blitAlpha(screen, pygame.transform.rotate(propulsionParticles, random.randrange(0, 360, 1)), propulsionParticleRect, 128)
            propulsionFade += 1
        else:
            propulsionParticleRect = pygame.Rect(-50, -50, 0, 0)
            propulsionFade = 0
        propulsionRect = pygame.Rect(Player.left-20, Player.top, 40,  40)
        screen.blit(propulsionImgLeft, propulsionRect)

    #DEBUG VALUES
    if debugSetting:
        frames = "FPS: " + str(int(clock.get_fps()))
        framesText = pygame.font.SysFont("Arial", 18).render(frames, 1, WHITE)
        screen.blit(framesText, (10, 0))

        #timer += 1/FPS
        #timerText = pygame.font.SysFont("Arial", 18).render("Time: " + str(timer), 1, WHITE)
        #screen.blit(timerText, (10, 20))

        #playerAccelXText = "Acceleration X: " + str(Player.accelX)
        #playerAccelX = pygame.font.SysFont("Arial", 18).render(playerAccelXText, 1, WHITE)
        #screen.blit(playerAccelX, (10, 40))

        #playerAccelYText = "Acceleration Y: " + str(Player.accelY)
        #playerAccelY = pygame.font.SysFont("Arial", 18).render(playerAccelYText, 1, WHITE)
        #screen.blit(playerAccelY, (10, 60))

        #vX1 = pygame.font.SysFont("Arial", 18).render("Velocity X: " + str(velocityX), 1, WHITE)
        #screen.blit(vX1, (10, 80))

        vY1 = pygame.font.SysFont("Arial", 18).render("Velocity Y: " + str(velocityY), 1, WHITE)
        screen.blit(vY1, (10, 100))

        #screen.blit(pygame.font.SysFont("Arial", 18).render("Friction X: " + str(frictionX), 1, WHITE), (10, 120))
        #screen.blit(pygame.font.SysFont("Arial", 18).render("Friction Y: " + str(frictionY), 1, WHITE), (10, 140))
        #screen.blit(pygame.font.SysFont("Arial", 18).render("Speed: " + str(speed), 1, WHITE), (10, 160))

    #Updates the thing to make it happen and go magically
    pygame.display.update()

    #ticks the clock forward for frame stuff
    clock.tick(FPS)
