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

def checkMultipleSquares(board, rowCount, colCount):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    safeSquares = []
    flagSquares = []
    checkLoop = True
    for row in range(0,rowCount):
        for col in range(0, colCount):
            currentAvailableSquares, currentMinesNeeded = getSquareDetails(board, rowCount, colCount, row, col)
            if currentAvailableSquares is None or currentMinesNeeded is None:
                continue
            elif currentMinesNeeded == 0:
                for move in currentAvailableSquares:
                    if move not in safeSquares:
                        checkLoop = False
                        safeSquares.append(move)
            elif len(currentAvailableSquares) == currentMinesNeeded:
                for move in currentAvailableSquares:
                    if move not in flagSquares:
                        checkLoop = False
                        print(move, ' flagged')
                        flagSquares.append(move)
            elif checkLoop:

                for direction in directions:
                    for i in range(1,3):
                        if checkLoop is False:
                            continue
                        print(currentAvailableSquares, 'current available', row, col)
                        nextRow = row + direction[0]*i
                        nextCol = col + direction[1]*i
                        if 0 <= nextRow < rowCount and 0 <= nextCol < colCount:
                            nextAvailableSquares, nextMinesNeeded = getSquareDetails(board, rowCount, colCount, nextRow, nextCol)
                            if nextAvailableSquares is None or nextMinesNeeded is None:
                                continue
                            elif nextMinesNeeded == 0:
                                for move in nextAvailableSquares:
                                    if move not in safeSquares:
                                        checkLoop = False
                                        safeSquares.append(move)
                                continue
                            elif len(nextAvailableSquares) == nextMinesNeeded:
                                for move in nextAvailableSquares:
                                    if move not in flagSquares:
                                        checkLoop = False
                                        print(move, ' flagged')
                                        flagSquares.append(move)
                                continue
                            elif nextAvailableSquares == currentAvailableSquares:
                                continue
                            elif len(nextAvailableSquares) == 0 or len(currentAvailableSquares) == 0:
                                continue
                            elif len(nextAvailableSquares) == len(currentAvailableSquares):
                                continue
                            elif len(nextAvailableSquares) > len(currentAvailableSquares):
                                longList = nextAvailableSquares.copy()
                                longMines = nextMinesNeeded
                                shortList = currentAvailableSquares.copy()
                                shortMines = currentMinesNeeded
                            elif  len(nextAvailableSquares) < len(currentAvailableSquares):
                                longList = currentAvailableSquares.copy()
                                longMines = currentMinesNeeded
                                shortList = nextAvailableSquares.copy()
                                shortMines = nextMinesNeeded
                            print(longList, shortList, longMines, shortMines, row, col, nextRow, nextCol)
                            counter = 0
                            for value in range(len(longList) - 1, -1, -1):
                                if longList[value] in shortList:
                                    print('matching')
                                    counter += 1
                                    longList.remove(longList[value])
                                elif longList[value] in safeSquares:
                                    print('safe')
                                    longList.remove(longList[value])
                                elif longList[value] in flagSquares:
                                    print('flag')
                                    longList.remove(longList[value])
                            if counter == len(shortList) and longMines == shortMines:
                                print(longList, shortList, longMines, shortMines, row, col, nextRow, nextCol, 'accepted')
                                for move in longList:
                                    if move not in flagSquares:
                                        print(move, 'safe by extra', longList, shortList, longMines, shortMines, row, col, nextRow, nextCol)
                                        safeSquares.append(move)

                            if len(longList) == (longMines - shortMines) and counter == len(shortList):
                                for move in longList:
                                    if move not in flagSquares:
                                        print(move, ' flagged by extra', longList, shortList, longMines, shortMines, row, col, currentAvailableSquares, nextRow, nextCol, nextAvailableSquares)
                                        flagSquares.append(move)
                            # if row == 1 and col == 13:
                            #     print(len(longList), (longMines - shortMines), counter, len(shortList))

    return flagSquares, safeSquares



def getSquareDetails(board, rowCount, colCount, row, col):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    if board[row][col] == 'flag' or board[row][col] == '-' or board[row][col] == 0:
        currentAvailableSquares = None
        currentMinesNeeded = None
    else:
        # print(row, col)
        currentAvailableSquares = []
        currentMinesNeeded = board[row][col]
        for direction in directions:
            endRow = row + direction[0]
            endCol = col + direction[1]
            if 0 <= endRow < rowCount and 0 <= endCol < colCount:
                if board[endRow][endCol] == '-':
                    currentAvailableSquares.append((endRow, endCol))
                elif board[endRow][endCol] == 'flag':
                    currentMinesNeeded -= 1
    return currentAvailableSquares, currentMinesNeeded



    #             possibleSquares.append(currentAvailableSquares)
    # for i in range(0, len(possibleSquares)):
    #     counter = 0
    #     currentCoords = possibleSquares[i]
    #     nextVal = i + 1
    #     previousVal = i + 1
    #     if 0 <= nextVal < len(possibleSquares):
    #         nextCoords = possibleSquares[nextVal]
    #         if len(currentCoords) > 0 and len(nextCoords) > 0:
    #             for item in currentCoords:
    #                 if item in safeSquares:
    #                     continue
    #                 elif item in nextCoords:
    #                     counter += 1
    #         print(currentCoords, nextCoords, counter)
    #
    # return possibleSquares


