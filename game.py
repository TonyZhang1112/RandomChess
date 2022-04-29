import pygame as pg
import random
import time
import chess

pg.init()

# CONSTANTS
DIMTILE = int(80)
userColor = chess.WHITE
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

# Set up chess screen window (100 x 100 pixels e/gameach tile)
screen = pg.display.set_mode([DIMTILE*8, DIMTILE*8])
timer = pg.time.Clock()

# Variables
reviewing = False
difficulty = int(0)
move = str('')
pieceSelected = None
board = chess.Board.from_chess960_pos(random.randint(0, 959))

# Used to choose move of user's turn
def selectMove(x: int, y: int):
    global move
    global pieceSelected
    square = chess.square(x//DIMTILE, 7-(y//DIMTILE))
    if (move == ''):
        if (board.piece_at(square) != None and board.piece_at(square).color == userColor):
            move += chess.square_name(square)
            pieceSelected = board.piece_at(square)
    else:
        legalMoves = legalMoves = list(board.legal_moves)
        dest = chess.square_name(chess.square(x//DIMTILE, 7-(y//DIMTILE)))
        if (dest[1] == '8' or dest[1] == '1') and pieceSelected.piece_type == chess.PAWN:
            dest += 'q'
        try:
            if board.parse_san(move+dest) in legalMoves:
                board.push(board.parse_san(move+dest))
                move = ""
                pieceSelected = None
        except:
            # Illegal Move
            move = ""
            pieceSelected = None

def botMovePicker():
    legalMoves = list(board.legal_moves)
    pick = random.randint(0, len(legalMoves)-1)
    move = legalMoves[pick]
    if move in board.legal_moves:
        board.push(move)

# EFFECTS: Creates text for buttons, helper
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
            global reviewing
            if function == "0":
                difficulty = 0
                mainGameScreen()
            elif function == "1":
                difficulty = 1
                mainGameScreen()
            elif function == "2":
                difficulty = 2
                mainGameScreen()
            elif function == "3":
                global board
                time.sleep(0.5)
                board = chess.Board.from_chess960_pos(random.randint(0, 959))
                reviewing = False
                startScreen()
            elif function == "4":
                reviewing = True
                mainGameScreen()
            elif function == "5":
                pg.quit()
                quit()
            else:
                reviewing = False
                if board.outcome().winner == chess.WHITE:
                    endScreen(0)
                elif board.outcome().winner == chess.BLACK:
                    endScreen(1)
                else:
                    endScreen(2)
            
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

    screen.blit(img, (x*DIMTILE + (DIMTILE-60)/2, y*DIMTILE + (DIMTILE-60)/2))

def startScreen():
    showMenu = True
    while showMenu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        
        mouse = pg.mouse.get_pos()
        screen.fill(white)
        
        #Intro Text
        makeText("RandomChess", DIMTILE*4, DIMTILE, 70, 'cambria')
        makeText("Choose a Difficulty:", DIMTILE*4, DIMTILE*2.25, 50, 'cambria')

        # Difficulty Buttons
        makeButton("Easy", DIMTILE*3, DIMTILE*3.25, DIMTILE*2, 50, green, bGreen, "0")
        makeButton("Medium", DIMTILE*3, DIMTILE*4.75, DIMTILE*2, 50, yellow, bYellow, "1")
        makeButton("Hard", DIMTILE*3, DIMTILE*6.25, DIMTILE*2, 50, red, bRed, "2")


        pg.display.update()
        timer.tick(30)

def mainGameScreen():
    isRunning = True
    sqrSelect = None
    while isRunning:
        if (move != ''):
            sqrSelect = chess.parse_square(move)
        else:
            sqrSelect = None

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if board.turn == userColor and reviewing == False:
                    selectMove(mouse[0], mouse[1])

        mouse = pg.mouse.get_pos()

        if board.outcome() and reviewing == False:
            if board.outcome().winner == chess.WHITE:
                endScreen(0)
            elif board.outcome().winner == chess.BLACK:
                endScreen(1)
            else:
                endScreen(2)


        screen.fill(green)

        for i in range (0, 8):
            for j in range (0, 8):
                square = chess.square(i, 7-j)
                if (i + j) % 2 == 0:
                    pg.draw.rect(screen, white, 
                    (i*DIMTILE, j*DIMTILE, DIMTILE, DIMTILE))
                if board.piece_at(square) != None and board.piece_at(square).piece_type == chess.KING and board.is_attacked_by(not board.piece_at(square).color, square):
                    pg.draw.rect(screen, bRed, 
                    (i*DIMTILE, j*DIMTILE, DIMTILE, DIMTILE))
                if sqrSelect != None and chess.square_distance(square, sqrSelect) == 0:
                    pg.draw.rect(screen, yellow, 
                    (i*DIMTILE, j*DIMTILE, DIMTILE, DIMTILE))
                if board.piece_at(square) != None:
                    drawPiece(i, j, board.piece_at(square))
                if (reviewing == True):
                    makeButton("Back", DIMTILE*3.5, DIMTILE*3.75, DIMTILE, 50, yellow, bYellow, "6")
        
        if board.turn != userColor and reviewing == False:
            pg.display.update()
            time.sleep(0.5)
            botMovePicker()

        pg.display.update()
        timer.tick(30)

# Displays when Checkmate or a Draw has been reached
def endScreen(outcome: int):
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        
        mouse = pg.mouse.get_pos()
        screen.fill(white)

        # White Won
        if (outcome == 0):
            makeText("White Wins!", DIMTILE*4, DIMTILE, 70, 'cambria')
            makeText("Checkmate on Black", DIMTILE*4, DIMTILE*2.25, 50, 'cambria')

        if (outcome == 1):
            makeText("Black Wins!", DIMTILE*4, DIMTILE, 70, 'cambria')
            makeText("Checkmate on White", DIMTILE*4, DIMTILE*2.25, 50, 'cambria')

        if (outcome == 2):
            makeText("Draw!", DIMTILE*4, DIMTILE, 70, 'cambria')
            match board.outcome().termination:
                case chess.Termination.STALEMATE:
                    makeText("Stalemate", DIMTILE*4, DIMTILE*2.25, 50, 'cambria')
                case chess.Termination.INSUFFICIENT_MATERIAL:
                    makeText("By Insufficient Material", DIMTILE*4, DIMTILE*2.25, 50, 'cambria')
                case chess.Termination.SEVENTYFIVE_MOVES:
                    makeText("By 75-move Rule", DIMTILE*4, DIMTILE*2.25, 50, 'cambria')
                case chess.Termination.FIVEFOLD_REPETITION:
                    makeText("By Fivefold Repetition", DIMTILE*4, DIMTILE*2.25, 50, 'cambria')
                case _:
                    makeText("ERROR", DIMTILE*4, DIMTILE*2.25, 50, 'cambria')

        # Endscreen Options
        makeButton("Play Again", DIMTILE*2, DIMTILE*3.25, DIMTILE*4, 50, green, bGreen, "3")
        makeButton("Review Board", DIMTILE*2, DIMTILE*4.75, DIMTILE*4, 50, yellow, bYellow, "4")
        makeButton("RAGE QUIT", DIMTILE*2, DIMTILE*6.25, DIMTILE*4, 50, red, bRed, "5")

        pg.display.update()
        timer.tick(30)




startScreen()

# User has Exit
pg.quit()
quit()
