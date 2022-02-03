'''
Find all safe moves for a current board.
May also implement something that can iterate those moves to make them.
Will probably just call doCLick
'''


def countAvailableSquares(board, rowCount, colCount):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    flagSquares = []
    safeSquares = []
    for row in range(0, rowCount):
        for col in range(0, colCount):
            squareVal = board[row][col]
            mineSquaresRemaining = squareVal
            if squareVal == '-':
                pass
            elif squareVal == 'flag':
                pass
            elif squareVal == 0:
                pass
            else:
                # print("square: ", row, col)
                emptySquares = []
                for direction in directions:
                    endRow = row + direction[0]
                    endCol = col + direction[1]
                    if 0 <= endRow < rowCount and 0 <= endCol < colCount and board[endRow][endCol] == 'flag':
                        mineSquaresRemaining -= 1
                    elif 0 <= endRow < rowCount and 0 <= endCol < colCount and board[endRow][endCol] == '-':
                        # print("adding:", (endRow, endCol), " to empty squares")
                        emptySquares.append((endRow, endCol))
                if mineSquaresRemaining == 0:
                    for square in emptySquares:
                        safeSquares.append(square)
                if len(emptySquares) == mineSquaresRemaining:
                    # print("length is same")
                    for square in emptySquares:
                        if square not in flagSquares:
                            flagSquares.append(square)
                else:
                    # print("length is different")
                    pass

    if len(flagSquares) == 0:
        flagSquares = None
    if len(safeSquares) == 0:
        safeSquares = None
    return flagSquares, safeSquares

