import pygame as p
from Minesweeper import MinesweeperEngine as mine

'''
Set up values.
Using a beginner board config as the starting point.
'''

p.init()
DIMENSION_Y = 9
DIMENSION_X = 9
MINES = 10
SQ_SIZE = 50
HEIGHT = DIMENSION_Y * SQ_SIZE
WIDTH = DIMENSION_X * SQ_SIZE
MAX_FPS = 15  # For animations later on
IMAGES = {}

DARK_GRAY = (50,50,50)

def loadImages():
    pieces = ['1', '2', '3', '4', '5', '6', '7', '8', 'flag', 'mine']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE - 10, SQ_SIZE - 10))

def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    loadImages()
    running = True
    gs = mine.GameState()
    gs.chooseMines(MINES, DIMENSION_X, DIMENSION_Y)
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
                    row = location[1] // SQ_SIZE
                    gs.doClick(row, col)
                elif pressed3:
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    gs.doFlagClick(row, col)
            #keys handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_SPACE:
                    gs.showEndState()
                if e.key == p.K_r and p.key.get_mods() & p.KMOD_CTRL:
                    gs = mine.GameState()
                    gs.chooseMines(MINES, DIMENSION_X, DIMENSION_Y)
                    gs.getSqaureValues()
                    screen.fill(p.Color("black"))

        drawGameState(screen, gs)

        if gs.gameOver:
            if gs.mineClicked:
                drawEndText(screen, "Game Over!")
            else:
                drawEndText(screen, "You win!")

        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawSquares(screen)  # draw squares on the board
    drawPieces(screen, gs.selectedBoard)  # draw pieces on top of the squares

def drawSquares(screen):
    for r in range(DIMENSION_X):
        for c in range(DIMENSION_Y):
            s = p.Surface((SQ_SIZE - 6, SQ_SIZE - 6))
            s.fill(p.Color('gray'))
            screen.blit(s, ((c * SQ_SIZE + 3), (r * SQ_SIZE + 3)))

def drawPieces(screen, board):
    for row in range(DIMENSION_X):
        for col in range(DIMENSION_Y):
            piece = board[row][col]
            if piece == 'x':  # not an empty square
                screen.blit(IMAGES['mine'], p.Rect(col * SQ_SIZE + 5, row * SQ_SIZE + 5, SQ_SIZE - 10, SQ_SIZE - 10))
            elif piece == 0:
                s = p.Surface((SQ_SIZE - 6, SQ_SIZE - 6))
                s.fill(p.Color(DARK_GRAY))
                screen.blit(s, ((col * SQ_SIZE + 3), (row * SQ_SIZE + 3)))
            elif piece != '-':
                piece = str(piece)
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE + 5, row * SQ_SIZE + 5, SQ_SIZE - 10, SQ_SIZE - 10))

def drawFinalPieces(screen, board):
    for row in range(DIMENSION_X):
        for col in range(DIMENSION_Y):
            piece = board[row][col]
            if piece == 'x':  # not an empty square
                screen.blit(IMAGES['mine'], p.Rect(col * SQ_SIZE + 5, row * SQ_SIZE + 5, SQ_SIZE - 10, SQ_SIZE - 10))
            elif piece != 0:
                piece = str(piece)
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE + 5, row * SQ_SIZE + 5, SQ_SIZE - 10, SQ_SIZE - 10))

def drawEndText(screen, text):
    font = p.font.SysFont("Helvitica", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2,2))

if __name__ == '__main__':
    main()