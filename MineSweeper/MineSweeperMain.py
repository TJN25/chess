import pygame as p
from Minesweeper import MinesweeperEngine as mine, findSafeSquares as fs
import neat

'''
Set up values.
Using a beginner board config as the starting point.
'''


p.init()
DIMENSION_ROWS = 15
DIMENSION_COLS = 15
GAP_SIZE = 2
MINES = 40
SQ_SIZE = 25
HEIGHT = DIMENSION_ROWS * SQ_SIZE + SQ_SIZE * 2
WIDTH = DIMENSION_COLS * SQ_SIZE
MAX_FPS = 15  # For animations later on
IMAGES = {}

DARK_GRAY = (100,100,100)

def loadImages():
    pieces = ['1', '2', '3', '4', '5', '6', '7', '8', 'flag', 'mine']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE - GAP_SIZE, SQ_SIZE - GAP_SIZE))

def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color(DARK_GRAY))
    loadImages()
    running = True
    gs = mine.GameState()
    gs.chooseMines(MINES, DIMENSION_ROWS, DIMENSION_COLS)
    gs.getSqaureValues()
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                pressed1 = p.mouse.get_pressed()[0]
                pressed3 = p.mouse.get_pressed()[2]
                if pressed1:
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // SQ_SIZE
                    row = (location[1] // SQ_SIZE) - 2
                    # print(row)
                    gs.doClick(row, col)
                elif pressed3:
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // SQ_SIZE
                    row = (location[1] // SQ_SIZE) - 2
                    gs.doFlagClick(row, col)
            #keys handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_SPACE:
                    if gs.gameOver:
                        pass
                    else:
                        availableSquares, safeSquares = fs.checkMultipleSquares(gs.selectedBoard, DIMENSION_ROWS, DIMENSION_COLS)
                        if availableSquares is None and safeSquares is None:
                            move = gs.getSafeSquare()
                            # possibleSquares = fs.checkMultipleSquares(gs.selectedBoard, DIMENSION_ROWS, DIMENSION_COLS)
                            # print(availableSquares)
                            # gs.doClick(move[0], move[1])
                        else:
                            if availableSquares is None:
                                print('None returned')
                                pass
                            else:
                                # print(availableSquares)
                                for move in availableSquares:
                                    # print(move)
                                    gs.doFlagClick(move[0], move[1])
                            if safeSquares is None:
                                print('No safe squares')
                            else:
                                # print(safeSquares)
                                for move in safeSquares:
                                    gs.doClick(move[0], move[1])

                if e.key == p.K_r and p.key.get_mods() & p.KMOD_CTRL:
                    gs = mine.GameState()
                    gs.chooseMines(MINES, DIMENSION_ROWS, DIMENSION_COLS)
                    gs.getSqaureValues()
                    screen.fill(p.Color(DARK_GRAY))
                if e.key == p.K_p:
                    print(gs.mineSquares)

        drawGameState(screen, gs)
        if gs.gameOver:
            if gs.mineClicked:
                drawEndText(screen, "Game Over!")
            else:
                drawEndText(screen, "You win!")
        else:
            availableSquares, safeSquares = fs.countAvailableSquares(gs.selectedBoard, DIMENSION_ROWS, DIMENSION_COLS)
            if availableSquares is None and safeSquares is None:
                move = gs.getSafeSquare()
                # print('using getSafeMove')
                # gs.doClick(move[0], move[1])

        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawSquares(screen)  # draw squares on the board
    drawPieces(screen, gs.selectedBoard)  # draw pieces on top of the squares
    drawHeaderRegion(screen, gs)


def drawSquares(screen):
    for r in range(DIMENSION_ROWS):
        for c in range(DIMENSION_COLS):
            s = p.Surface((SQ_SIZE - GAP_SIZE, SQ_SIZE - GAP_SIZE))
            s.fill(p.Color('gray'))
            screen.blit(s, ((c * SQ_SIZE + GAP_SIZE), (r * SQ_SIZE + GAP_SIZE + 2 * SQ_SIZE)))

def drawPieces(screen, board):
    for row in range(DIMENSION_ROWS):
        for col in range(DIMENSION_COLS):
            piece = board[row][col]
            if piece == 'x':  # not an empty square
                s = p.Surface((SQ_SIZE, SQ_SIZE))
                s.fill(p.Color('black'))
                screen.blit(s, ((col * SQ_SIZE), (row * SQ_SIZE+ 2 * SQ_SIZE)))

                s = p.Surface((SQ_SIZE - GAP_SIZE, SQ_SIZE - GAP_SIZE))
                s.fill(p.Color(DARK_GRAY))
                screen.blit(s, ((col * SQ_SIZE + GAP_SIZE), (row * SQ_SIZE + GAP_SIZE + 2 * SQ_SIZE)))
                screen.blit(IMAGES['mine'], p.Rect(col * SQ_SIZE + GAP_SIZE, row * SQ_SIZE + GAP_SIZE + 2 * SQ_SIZE, SQ_SIZE - GAP_SIZE, SQ_SIZE - GAP_SIZE))
            elif piece == 0:
                s = p.Surface((SQ_SIZE, SQ_SIZE))
                s.fill(p.Color('black'))
                screen.blit(s, ((col * SQ_SIZE), (row * SQ_SIZE + 2 * SQ_SIZE)))

                s = p.Surface((SQ_SIZE - GAP_SIZE, SQ_SIZE - GAP_SIZE))
                s.fill(p.Color(DARK_GRAY))
                screen.blit(s, ((col * SQ_SIZE + GAP_SIZE), (row * SQ_SIZE + GAP_SIZE + 2 * SQ_SIZE)))
            elif piece != '-':
                s = p.Surface((SQ_SIZE, SQ_SIZE))
                s.fill(p.Color('black'))
                screen.blit(s, ((col * SQ_SIZE), (row * SQ_SIZE + 2 * SQ_SIZE)))

                s = p.Surface((SQ_SIZE - GAP_SIZE, SQ_SIZE - GAP_SIZE))
                s.fill(p.Color(DARK_GRAY))
                screen.blit(s, ((col * SQ_SIZE + GAP_SIZE), (row * SQ_SIZE + GAP_SIZE + 2 * SQ_SIZE)))
                piece = str(piece)
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE + GAP_SIZE, row * SQ_SIZE + GAP_SIZE + 2 * SQ_SIZE, SQ_SIZE - GAP_SIZE, SQ_SIZE - GAP_SIZE))

def drawFinalPieces(screen, board):
    for row in range(DIMENSION_ROWS):
        for col in range(DIMENSION_COLS):
            piece = board[row][col]
            if piece == 'x':  # not an empty square
                screen.blit(IMAGES['mine'], p.Rect(col * SQ_SIZE + GAP_SIZE, row * SQ_SIZE + GAP_SIZE, SQ_SIZE - GAP_SIZE, SQ_SIZE - GAP_SIZE))
            elif piece != 0:
                piece = str(piece)
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE + GAP_SIZE, row * SQ_SIZE + GAP_SIZE, SQ_SIZE - GAP_SIZE, SQ_SIZE - GAP_SIZE))

def drawHeaderRegion(screen, gs):
    s = p.Surface((SQ_SIZE * DIMENSION_COLS, SQ_SIZE *2))
    s.fill(p.Color('grey'))
    screen.blit(s, (0,0))
    font = p.font.SysFont("Helvitica", 32, True, False)
    squaresRemaining = gs.getSquaresRemaining()
    minesRemaining = gs.getMinesRemaining()
    textSquares = font.render('S: ' + str(squaresRemaining), 0, p.Color('black'))
    textMines = font.render('M: ' + str(minesRemaining), 0, p.Color('black'))
    textSquaresLocation = p.Rect(0,0, WIDTH, HEIGHT).move(SQ_SIZE, textSquares.get_height()/2)
    textMinesLocation = p.Rect(0,0, WIDTH, HEIGHT).move(WIDTH - textMines.get_width() - SQ_SIZE, textMines.get_height()/2)
    screen.blit(textSquares, textSquaresLocation)
    screen.blit(textMines, textMinesLocation)





    # textLocation = p.Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)



def drawEndText(screen, text):
    font = p.font.SysFont("Helvitica", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2,  textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2,2))

if __name__ == '__main__':
    main()