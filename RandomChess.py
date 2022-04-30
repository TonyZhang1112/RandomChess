'''
RandomChess
Created by Tony Zhang

Face off against three different levels of bots in a game of chess where the backrank configuation is random (but symettrical)

Difficulties:
Easy: A Greedy Bot, will always play the move that looks the best without even considering what the opponent may do. Will always detect a Mate in One.
Medium: Slightly better than Easy, the medium bot will look at what the opponent may do, but not much further. Will always detect a Mate in Two.
Hard: Looks further ahead. Will always detect a Mate in Four.
'''

from cmath import inf
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
            move = chess.square_name(square)
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

'''
 Returns a value to add to the pieceValue in evaluatePosition.
 Note that 1 <= x <= 8, 1 <= y <= 8, and that x = 1, y = 1 represents square A1.

 Summary:
 - Knights on the borders are bad. Knights in the center are good.
 - Bishops on the borders are bad. Bishops in the center are good.
 - Rooks are good in the backrank's center, and in the second rank of the opponent's territory
 - Queens on the borders are slightly worse. Queens in the corners are bad.
 - Kings are bad anywhere that aren't their backrank corners.
 - Pawns are good in the center, and are very good close to the promotion square.
    - Central pawns in the default position (d and e file) are bad.
'''
def PiecePosition(piece: chess.Piece, x: int, y: int)->int:
    if piece.piece_type == chess.KNIGHT:
        if (x == 1 or x == 8) and (y == 1 or y == 8):
            return -50
        elif x == 1 or x == 8 or y == 1 or y == 8:
            return -30
        elif (x == 4 or x == 5) and (y == 4 or y == 5):
            return 20
        elif (x >= 3 or x <= 6) and (y >= 3 or y <= 6):
            return 10
        else:
            return 0
    elif piece.piece_type == chess.BISHOP:
        if (x == 1 or x == 8) and (y == 1 or y == 8):
            return -20
        elif x == 1 or x == 8 or y == 1 or y == 8:
            return -10
        elif (x >= 3 or x <= 6) and (y >= 3 or y <= 6):
            return 10
        else: return 0
    elif piece.piece_type == chess.KING:
        if piece.color == chess.BLACK:
            if y < 7: return -50
            elif x < 3 or x > 6: return 20
            else: return 0
        else:
            if y > 2: return -50
            elif x < 3 or x > 6: return 20
            else: return 0
    elif piece.piece_type == chess.QUEEN:
        if (x == 1 or x == 8) and (y == 1 or y == 8):
            return -20
        elif x == 1 or x == 8 or y == 1 or y == 8:
            return -10
        elif (x >= 3 or x <= 6) and (y >= 3 or y <= 6):
            return 5
        else: return 0
    elif piece.piece_type == chess.ROOK:
        if piece.color == chess.BLACK:
            if y == 2: return 10
            elif y == 8 and (x == 4 or x == 5): return 5
            else: return 0
        else: 
            if y == 7: return 10
            elif y == 1 and (x == 4 or x == 5): return 5
            else: return 0
    else:
        if piece.color == chess.BLACK:
            if y == 2: return 50
            elif y < 6 and (x == 4 or x == 5): return 25
            elif y == 3: return 15
            elif y == 7 and (x == 4 or x == 5): return -20
            else: return 0
        else: 
            if y == 7: return 50
            elif y > 3 and (x == 4 or x == 5): return 25
            elif y == 6: return 15
            elif y == 2 and (x == 4 or x == 5): return -20
            else: return 0

# Evaluates a position based on the pieces on the board
# Negative evaluations are favorable towards black, positive towards white
def evaluatePosition(board: chess.Board)->int:
    totalEval = int(0)
    if board.outcome():
        if board.outcome().winner == chess.WHITE: return 50000
        elif board.outcome().winner == chess.BLACK: return -50000
        else: return 0
    for i in range(0, 8):
        for j in range(0, 8):
            pieceValue = int(0)
            square = chess.square(i, 7-j)
            if board.piece_at(square) != None:
                if board.piece_at(square).piece_type == chess.PAWN:
                    pieceValue = 100
                elif board.piece_at(square).piece_type == chess.QUEEN:
                    pieceValue = 900
                elif board.piece_at(square).piece_type == chess.KING:
                    pieceValue = 10000
                elif board.piece_at(square).piece_type == chess.ROOK:
                    pieceValue = 500
                else:
                    pieceValue = 300

                # Incorporate piece positioning
                pieceValue += PiecePosition(board.piece_at(chess.square(i, 7-j)), i + 1, 8-j)
            
                if board.piece_at(chess.square(i, 7-j)).color == chess.WHITE:
                    totalEval += pieceValue
                else:
                    totalEval -= pieceValue
    return totalEval

# Chooses bot moves for easy difficulty
def easyMovePicker()->chess.Move:
    legalMoves = list(board.legal_moves)
    bestMoveIndex = int(0)
    bestMoveEval = int(99999)
    for index in range (0, len(legalMoves)-1):
        board.push(legalMoves[index])
        if evaluatePosition(board) < bestMoveEval:
            bestMoveEval = evaluatePosition(board)
            bestMoveIndex = index
        elif (evaluatePosition(board) == bestMoveEval):
            if random.randint(0, 1) == 0:
                bestMoveEval = evaluatePosition(board)
                bestMoveIndex = index
        board.pop()
    return legalMoves[bestMoveIndex]

            
# Chooses moves for medium and hard bots
# Setting: 0 for player, 1 for bot
def otherMovePicker(depth: int, setting: int, brd: chess.Board, alpha: int, beta: int)->chess.Move:
    if depth == 0: return None, evaluatePosition(brd)

    legalMoves = list(brd.legal_moves)
    if len(legalMoves) == 1:
        return legalMoves[0], evaluatePosition(brd)
    bestMove = None
    if (setting == 1):
        maxEval = 99999
        for move in legalMoves:
            brd.push(move)
            eval = otherMovePicker(depth-1, 0, brd, alpha, beta)[1]
            brd.pop()
            if (eval < maxEval):
                maxEval = eval
                bestMove = move
            alpha = min(alpha, eval)
            if beta >= alpha:
                break
        return bestMove, maxEval
    
    else:
        minEval = -99999
        for move in legalMoves:
            brd.push(move)
            eval = otherMovePicker(depth-1, 1, brd, alpha, beta)[1]
            brd.pop()
            if (eval > minEval):
                minEval = eval
                bestMove = move
            beta = max(beta, eval)
            if beta >= alpha:
                break
        return bestMove, minEval
            



# Choose a move-picking method based on the difficulty chosen
def botMovePicker():
    if difficulty == 0:
        move = easyMovePicker()
        board.push(move)
    elif difficulty == 1:
        move = otherMovePicker(2, 1, board, inf, -inf)[0]
        board.push(move)
    else:
        move = otherMovePicker(4, 1, board, inf, -inf)[0]
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
                time.sleep(0.2)
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
                time.sleep(0.5)
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

# Main Menu
def startScreen():
    while True:
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

# In Game
def mainGameScreen():
    sqrSelect = None
    while True:
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
            time.sleep(0.2)
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
        
        screen.fill(white)

        # White Won
        if (outcome == 0):
            makeText("White Wins!", DIMTILE*4, DIMTILE, 70, 'cambria')
            makeText("Checkmate on Black", DIMTILE*4, DIMTILE*2.25, 50, 'cambria')

        # Black Won
        if (outcome == 1):
            makeText("Black Wins!", DIMTILE*4, DIMTILE, 70, 'cambria')
            makeText("Checkmate on White", DIMTILE*4, DIMTILE*2.25, 50, 'cambria')

        # Draw
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

# Starts the Main Menu
startScreen()
