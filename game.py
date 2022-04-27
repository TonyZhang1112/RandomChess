
import pygame as pg
import random
import time


pg.init()



# CONSTANTS
DIMTILE = 100
green = (0, 179, 0)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (200, 200, 0)
red = (150, 0, 0)

bRed = (255, 0, 0)
bYellow = (255, 255, 0)
bGreen = (0, 255, 0)

#set up chess board window (100 x 100 pixels e/gameach tile)
board = pg.display.set_mode([DIMTILE*8, DIMTILE*8])
timer = pg.time.Clock()

# Variables
difficulty = 0
piecePlacement = []
isRunning = True
showMenu = True

#Event Handling
def handleEvent(x, y):
    #showMenu = False
    print("Hi")

def makeTxt(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def startScreen():
    while showMenu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                handleEvent(mouse[0], mouse[1])
        
        mouse = pg.mouse.get_pos()
        board.fill(white)
        titleText = pg.font.SysFont('cambria',70)
        TextSurf, TextRect = makeTxt("RandomChess", titleText)
        TextRect.center = (DIMTILE*4, DIMTILE)
        board.blit(TextSurf, TextRect)

        chooseText = pg.font.SysFont('cambria', 50)
        textSurf, textRect = makeTxt("Choose a Difficulty:", chooseText)
        textRect.center = (400, 225)
        board.blit(textSurf, textRect)

        #buttons that lighten up when hovered over
        if (300 <= mouse[0] <= 500 and 300 <= mouse[1] <= 350):
            pg.draw.rect(board, bGreen, (300, 300, 200, 50))
        else:
            pg.draw.rect(board, green, (300, 300, 200, 50))

        if (300 <= mouse[0] <= 500 and 450 <= mouse[1] <= 500):
            pg.draw.rect(board, bYellow, (300, 450, 200, 50))
        else:
            pg.draw.rect(board, yellow, (300, 450, 200, 50))

        if (300 <= mouse[0] <= 500 and 600 <= mouse[1] <= 650):
            pg.draw.rect(board, bRed, (300, 600, 200, 50))
        else:
            pg.draw.rect(board, red, (300, 600, 200, 50))

        
        buttonText = pg.font.SysFont('cambria', 40)
        textSurf, textRect = makeTxt("Easy", buttonText)
        textRect.center = (400, 324)
        board.blit(textSurf, textRect)

        buttonText = pg.font.SysFont('cambria', 40)
        textSurf, textRect = makeTxt("Medium", buttonText)
        textRect.center = (400, 474)
        board.blit(textSurf, textRect)

        buttonText = pg.font.SysFont('cambria', 40)
        textSurf, textRect = makeTxt("Hard", buttonText)
        textRect.center = (400, 624)
        board.blit(textSurf, textRect)

        pg.display.update()
        timer.tick(30)



def mainGameScreen():
    while isRunning:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                isRunning = False
            if event.type == pg.MOUSEBUTTONDOWN:
                handleEvent(mouse[0], mouse[1])

        mouse = pg.mouse.get_pos()

        if inGame:
            board.fill(green)

            for i in range (0, 8):
                for j in range (0, 8):
                    if ((i + j) % 2 == 0):
                        pg.draw.rect(board, white, 
                        (i*DIMTILE, j*DIMTILE, DIMTILE, DIMTILE))
        
        else:
            startScreen()
        pg.display.update()
        timer.tick(30)

startScreen()
mainGameScreen()

# User has Exit
pg.quit()
quit()
