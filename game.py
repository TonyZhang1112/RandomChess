import pygame as pg
import random
import time
import chess

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

# Piece images
bp = pg.image.load('images\BlackPawn.png')
br = pg.image.load('images\BlackRook.png')
bn = pg.image.load('images\BlackKnight.png')
bk = pg.image.load('images\BlackKing.png')
bq = pg.image.load('images\BlackQueen.png')
bp = pg.image.load('images\BlackBishop.png')
wp = pg.image.load('images\WhitePawn.png')
wr = pg.image.load('images\WhiteRook.png')
wn = pg.image.load('images\WhiteKnight.png')
wk = pg.image.load('images\WhiteKing.png')
wq = pg.image.load('images\WhiteQueen.png')
wp = pg.image.load('images\WhiteBishop.png')

#set up chess screen window (100 x 100 pixels e/gameach tile)
screen = pg.display.set_mode([DIMTILE*8, DIMTILE*8])
timer = pg.time.Clock()

# Variables
difficulty = 0
board = chess.Board.from_chess960_pos(random.randint(0, 959))
print(board)
print(board.legal_moves)
isRunning = True
showMenu = True

#Event Handling
def handleEvent(x, y):
    #showMenu = False
    print("Hi")

#EFFECTS: Creates text for buttons, helper
def makeTxt(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def makeButton(txt, x, y, w, h, default, hover):
    mouse = pg.mouse.get_pos()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pg.draw.rect(screen, hover,(x,y,w,h))
    else:
        pg.draw.rect(screen, default,(x,y,w,h))

    buttonText = pg.font.SysFont("cambria", 40)
    tSurf, tRect = makeTxt(txt, buttonText)
    tRect.center = ((x+(w/2)), (y+(h/2))-1)
    screen.blit(tSurf, tRect)

#MODIFIES: screen
#EFFECTS: Creates text centered at x, y, with font size s and font f
def makeText(txt, x, y, s, f):
    text = pg.font.SysFont(f, s)
    TSurf, TRect = makeTxt(txt, text)
    TRect.center = (x, y)
    screen.blit(TSurf, TRect)

def startScreen():
    while showMenu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                handleEvent(mouse[0], mouse[1])
        
        mouse = pg.mouse.get_pos()
        screen.fill(white)
        
        #Intro Text
        makeText("RandomChess", DIMTILE*4, DIMTILE, 70, 'cambria')
        makeText("Choose a Difficulty:", DIMTILE*4, DIMTILE*2.25, 50, 'cambria')

        # Difficulty Buttons
        makeButton("Easy", DIMTILE*3, DIMTILE*3, DIMTILE*2, 50, green, bGreen)
        makeButton("Medium", DIMTILE*3, DIMTILE*4.5, DIMTILE*2, 50, yellow, bYellow)
        makeButton("Hard", DIMTILE*3, DIMTILE*6, DIMTILE*2, 50, red, bRed)


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


        screen.fill(green)

        for i in range (0, 8):
            for j in range (0, 8):
                if ((i + j) % 2 == 0):
                    pg.draw.rect(screen, white, 
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
