import pygame as pg
import random
import time
import chess

pg.init()

# CONSTANTS
DIMTILE = 80
green = (0, 179, 0)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (200, 200, 0)
red = (150, 0, 0)

bRed = (255, 0, 0)
bYellow = (255, 255, 0)
bGreen = (0, 255, 0)

# Piece images
bpIMG = pg.image.load('images\BlackPawn.png')
brIMG = pg.image.load('images\BlackRook.png')
bnIMG = pg.image.load('images\BlackKnight.png')
bkIMG = pg.image.load('images\BlackKing.png')
bqIMG = pg.image.load('images\BlackQueen.png')
bbIMG = pg.image.load('images\BlackBishop.png')
wpIMG = pg.image.load('images\WhitePawn.png')
wrIMG = pg.image.load('images\WhiteRook.png')
wnIMG = pg.image.load('images\WhiteKnight.png')
wkIMG = pg.image.load('images\WhiteKing.png')
wqIMG = pg.image.load('images\WhiteQueen.png')
wbIMG = pg.image.load('images\WhiteBishop.png')

#set up chess screen window (100 x 100 pixels e/gameach tile)
screen = pg.display.set_mode([DIMTILE*8, DIMTILE*8])
timer = pg.time.Clock()

# Variables
difficulty = 0
board = chess.Board.from_chess960_pos(random.randint(0, 959))
legalMoves = list(board.legal_moves)
print(legalMoves[random.randint(0, len(legalMoves)-1)])
move = legalMoves[random.randint(0, len(legalMoves)-1)]
if move in board.legal_moves:
    board.push(move)
    print(board)
print(board.piece_at(chess.B4))
print(board.generate_legal_moves())

#Event Handling
def handleEvent(x, y):
    print(difficulty)

#EFFECTS: Creates text for buttons, helper
def makeTxt(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def makeButton(txt, x, y, w, h, default, hover, function=None):
    mouse = pg.mouse.get_pos()
    press = pg.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pg.draw.rect(screen, hover,(x,y,w,h))
        if press[0] == 1 and function != None:
            global difficulty
            if function == "0":
                difficulty = 0
            elif function == "1":
                difficulty = 1
            else:
                difficulty = 2
            mainGameScreen()
            
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

#int, int, Piece -> None
#Draws the given piece at tile (x, y)
def drawPiece(x, y, piece):
    img = bpIMG
    if (piece.color == chess.WHITE):
        if piece.piece_type == chess.PAWN:
            img = wpIMG
        elif piece.piece_type == chess.BISHOP:
            img = wbIMG
        elif piece.piece_type == chess.KNIGHT:
            img = wnIMG
        elif piece.piece_type == chess.QUEEN:
            img = wqIMG
        elif piece.piece_type == chess.KING:
            img = wkIMG
        elif piece.piece_type == chess.ROOK:
            img = wrIMG
    else:
        if piece.piece_type == chess.BISHOP:
            img = bbIMG
        elif piece.piece_type == chess.KNIGHT:
            img = bnIMG
        elif piece.piece_type == chess.QUEEN:
            img = bqIMG
        elif piece.piece_type == chess.KING:
            img = bkIMG
        elif piece.piece_type == chess.ROOK:
            img = brIMG

    screen.blit(img, (x*DIMTILE + 10, y*DIMTILE + 10))

def startScreen():
    showMenu = True
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
        makeButton("Easy", DIMTILE*3, DIMTILE*3, DIMTILE*2, 50, green, bGreen, "0")
        makeButton("Medium", DIMTILE*3, DIMTILE*4.5, DIMTILE*2, 50, yellow, bYellow, "1")
        makeButton("Hard", DIMTILE*3, DIMTILE*6, DIMTILE*2, 50, red, bRed, "2")


        pg.display.update()
        timer.tick(30)

def mainGameScreen():
    isRunning = True
    while isRunning:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                handleEvent(mouse[0], mouse[1])

        mouse = pg.mouse.get_pos()


        screen.fill(green)

        for i in range (0, 8):
            for j in range (0, 8):
                global board
                square = chess.square(i, 7-j)
                if ((i + j) % 2 == 0):
                    pg.draw.rect(screen, white, 
                    (i*DIMTILE, j*DIMTILE, DIMTILE, DIMTILE))
                if board.piece_at(square) != None:
                    drawPiece(i, j, board.piece_at(square))
        
        
        pg.display.update()
        timer.tick(30)

startScreen()

# User has Exit
pg.quit()
quit()
