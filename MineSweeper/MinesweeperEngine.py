import random, math

'''
Class containing gamestate with the board details
'''

class GameState():


    def __init__(self):
        self.board = [
            ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-']
        ]
        self.selectedBoard = [
            ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-']
        ]
        self.mineSquares = []
        self.xLength = 9
        self.yLength = 9
        self.mineClicked = False
        self.minesFlagged = 0
        self.gameOver = False


    '''
    Set the board dimensions with blank mines based on DIMENSION_X and DIMENSION_Y
    Get total number of squares for mine selection
    '''



    def chooseMines(self, mines, xLength, yLength):
        self.mineSquares = random.sample(range(xLength*yLength), mines)
        print(self.mineSquares)
        for selectedSq in self.mineSquares:
            row = math.floor(selectedSq / xLength)
            col = selectedSq % yLength
            print(row, col, self.board[row][col])
            self.board[row][col] = 'x'


    def getSqaureValues(self):
        directions = [(0,1), (1,0), (0, -1), (-1, 0), (1,1), (-1,-1), (-1, 1), (1, -1)]
        for row in range(0, self.xLength):
            for col in range(0, self.yLength):
                if self.board[row][col] == '-':
                    mineCounter = 0
                    for direction in directions:
                        endRow = row + direction[0]
                        endCol = col + direction[1]
                        if 0 <= endRow < self.xLength and 0 <= endCol < self.yLength and self.board[endRow][endCol] == 'x':
                            mineCounter += 1
                    self.board[row][col] = mineCounter

    def doClick(self, row, col):
        if self.selectedBoard[row][col] == 'flag':
            return
        clickValue = self.board[row][col]
        if clickValue == 'x':
            self.gameOver = True
            self.mineClicked = True
            self.showEndState()
        if clickValue == 0:
            self.selectedBoard[row][col] = clickValue
            self.setAllZeros(row, col)
        self.selectedBoard[row][col] = clickValue

    def doFlagClick(self, row, col):
        clickValue = self.board[row][col]
        currentValue = self.selectedBoard[row][col]
        if currentValue == 'flag':
            self.selectedBoard[row][col] = '-'
            if clickValue == 'x':
                self.minesFlagged -= 1
        else:
            self.selectedBoard[row][col] = 'flag'
            if clickValue == 'x':
                self.minesFlagged += 1
                if self.minesFlagged == len(self.mineSquares):
                    self.gameOver = True

    def setAllZeros(self, row, col):
        directions = [(0,1), (1,0), (0, -1), (-1, 0)]
        extraDirections = [(1,1), (-1,-1), (-1, 1), (1, -1)]
        checkDiagonals = False
        for direction in directions:
            endRow = row + direction[0]
            endCol = col + direction[1]
            if 0 <= endRow < self.xLength and 0 <= endCol < self.yLength and self.selectedBoard[endRow][endCol] == 0:
                continue
            elif 0 <= endRow < self.xLength and 0 <= endCol < self.yLength and self.board[endRow][endCol] == 0:
                print(endRow, endCol)
                checkDiagonals = True
                self.selectedBoard[endRow][endCol] = 0
                self.setAllZeros(endRow, endCol)
            elif 0 <= endRow < self.xLength and 0 <= endCol < self.yLength:
                print(endRow, endCol)
                self.selectedBoard[endRow][endCol] = self.board[endRow][endCol]
        if checkDiagonals:
            for direction in extraDirections:
                endRow = row + direction[0]
                endCol = col + direction[1]
                if 0 <= endRow < self.xLength and 0 <= endCol < self.yLength and self.selectedBoard[endRow][endCol] == 0:
                    continue
                elif 0 <= endRow < self.xLength and 0 <= endCol < self.yLength and self.board[endRow][endCol] == 0:
                    print(endRow, endCol)
                    self.selectedBoard[endRow][endCol] = 0
                    self.setAllZeros(endRow, endCol)
                elif 0 <= endRow < self.xLength and 0 <= endCol < self.yLength:
                    print(endRow, endCol)
                    self.selectedBoard[endRow][endCol] = self.board[endRow][endCol]
        else:
            for direction in extraDirections:
                endRow = row + direction[0]
                endCol = col + direction[1]
                if 0 <= endRow < self.xLength and 0 <= endCol < self.yLength and self.board[endRow][endCol] != 0:
                    self.selectedBoard[endRow][endCol] = self.board[endRow][endCol]
        return


    def showEndState(self):
        self.selectedBoard = self.board

