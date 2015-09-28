# ----------------------------------#
# PygamePong.py by Joshua A. Jacobs #
# http://joshalexjacobs.github.io/  #
# ----------------------------------#

# To compile and run:
# 1. Ensure that Python 2.7 is installed
# 2. Open a console in PygamePong.py's directory
# 3. Run "python pygamepong.py"

# Future additions:
# - update score 
# - a simple cursor
# - arrow key and wasd controlls
# - a 2 player mode
# - ball will increase speed after X bounces (similar to the original atari pong)

import pygame, sys, random, math
from pygame.locals import *

# number of frames per second
# change this value to speed up or slow down your game
FPS = 200

# global variables to be used through-out our program
WINDOWWIDTH = 400 # our window's width...
WINDOWHEIGHT = 300 # and our window's height
LINETHICKNESS = 7 # used to determine thickness of lines
PADDLESIZE = 50 # length of the paddle
PADDLEOFFSET = 20 # the distance the paddle is from the arena edges

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# classes
class Ball:
    def __init__(self, (x, y), size): # here we define our object's variables
        self.x = x # the ball's x coordinate...
        self.y = y # and it's y coordinate
        self.size = size # the size of our ball (aka radius)
        self.color = (WHITE) 
        self.thickness = 4 # the thickness of our ball's lines
        self.speed = 1.5 # our ball's default speed
        self.angle = 2
        
    def display(self): # this function is used to draw this ball 
        pygame.draw.circle(DISPLAYSURF, self.color, (int(self.x), int(self.y)), self.size, self.thickness)
        
    # this function is used to move this ball
    # NOTE: angles are in radians. fortunately math has a pi function
    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        
    def bounce(self): # if the ball collides with a wall, bounce it
        if self.x > WINDOWWIDTH - self.size:
            self.x = 2 * (WINDOWWIDTH - self.size) - self.x
            self.angle = - self.angle
        
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle
        
        if self.y > WINDOWHEIGHT - self.size:
            self.y = 2 * (WINDOWHEIGHT - self.size) - self.y
            self.angle = math.pi - self.angle
        
        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
    
    def collidePaddles(self, paddle1, paddle2):
        # if the ball collides with the player's paddle, bounce the ball
        if paddle1.colliderect(pygame.Rect(self.x, self.y, self.size, self.size)):
            if self.x < paddle1.right - self.size:
                self.x = 2 * (paddle1.right - self.size) - self.x
                self.angle = - self.angle
        # if the ball colides with the ai's paddle, bounce the ball
        elif paddle2.colliderect(pygame.Rect(self.x, self.y, self.size, self.size)):
            if self.x > paddle2.left - self.size:
                self.x = 2 * (paddle2.left - self.size) - self.x
                self.angle = - self.angle

# draws the arena the game will be played in
def drawArena():
    DISPLAYSURF.fill(BLACK)
    # draw center line
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH / 2), 0), ((WINDOWWIDTH / 2), WINDOWHEIGHT), (LINETHICKNESS / 4))

# draws the paddle
def drawPaddle(paddle):
    # stops the paddle from moving out of bounds
    if paddle.bottom > WINDOWHEIGHT:
      paddle.bottom = WINDOWHEIGHT
    elif paddle.top < 0:
      paddle.top = 0
    
    # draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)  

def artificialIntelligence(ball, paddle2): 
    # convert ball.angle (radian) to degrees
    degrees = (ball.angle * 180) / math.pi
    
    # keep degrees in scope of 0 to 360 OR 0 to - 360
    while degrees > 360 or degrees < -360:
        if degrees > 360:
            degrees = degrees - 360
        elif degrees < -360:
            degrees = degrees + 360
            
     #if ball.angle >= 0 and ball.angle < math.pi:
    if degrees <= -1 and degrees >= -179 or degrees >= 181 and degrees <= 359:
      if paddle2.centery < (WINDOWHEIGHT/2):
        paddle2.y += 1
      elif paddle2.centery > (WINDOWHEIGHT/2):
        paddle2.y -= 1    
    
    #if ball.angle >= math.pi and ball.angle < math.pi * 2:
    if degrees >= 1 and degrees <= 179 or degrees <= -181 and degrees >= -359:
      if paddle2.centery < ball.y:
        paddle2.y += 1
      else:
        paddle2.y -= 1
    
    return paddle2
    
#Displays the current score on the screen for both players
def displayScore(playerOneScore, playerTwoScore):
    resultSurf = BASICFONT.render('%s    %s' %(playerOneScore, playerTwoScore), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 250, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)
	
def main():
    pygame.init() # initializes pygame
    global DISPLAYSURF # our global display surface that we will need to modify later on
    
    # Font information
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 50
    BASICFONT = pygame.font.Font('C:\Windows\Fonts\GILC____.TTF', BASICFONTSIZE)

    FPSCLOCK = pygame.time.Clock() # the pygame.time.Clock object allows the user to set their own framerate
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) # sets DISPLAYSURF and creates the pygame window
    pygame.display.set_caption('Pygame Pong') # sets the title of the window to read "Pong"
    
    # initiate variable and set starting positions
    # any future changes made within rectangles
    ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) /2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) /2
    
    playerOneScore = 0
    playerTwoScore = 0
    
    # creates rectangles for the ball and paddles
    paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, LINETHICKNESS, PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS, PADDLESIZE)
    newBall = Ball((ballX, ballY), 4) # new ball
    
    # draws the starting position of the Arena
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    
    pygame.mouse.set_visible(0) # make the cursor invisible
    
    while True: # main game loop
		
      for event in pygame.event.get(): # ensure the user can quit by closing the window
          if event.type == QUIT:
              pygame.quit()
              sys.exit()
			
          # mouse movement commands
          elif event.type == MOUSEMOTION:
              mousex, mousey = event.pos
              paddle1.y = mousey
		
      # updates arena each tick
      drawArena()
      drawPaddle(paddle1)
      drawPaddle(paddle2)
      
      # updates newBall each tick
      newBall.move()
      newBall.bounce()
      newBall.collidePaddles(paddle1, paddle2)
      newBall.display()
      
      paddle2 = artificialIntelligence(newBall, paddle2)
      
      displayScore(playerOneScore, playerTwoScore)
      
      pygame.display.update()
      FPSCLOCK.tick(FPS) # tells pygame how fast the game should run (should be called every tick)
		
if __name__=='__main__':
    main()