import random

pieceScores = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
kingScores = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0.5, 1.5, 1, 0, 0, 0, 1, 0.5]
]

queenScores = [
            [9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9]
]

rookScores = [
            [6, 6, 6, 6, 6, 6, 6, 6],
            [7, 7, 7, 7, 7, 7, 7, 7],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 5, 4, 5, 4, 4]
]

bishopScores = [
            [3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3],
            [3, 4, 3, 3, 3, 3, 4, 3],
            [3, 3, 4, 4, 4, 4, 3, 3],
            [3, 3, 4, 4, 4, 4, 3, 3],
            [3, 4, 3, 3, 3, 3, 4, 3],
            [3, 3, 3, 3, 3, 3, 3, 3],
]


knightScores = [
            [3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 4, 3, 3, 3],
            [3, 3, 4.5, 3, 3, 4.5, 3, 3],
            [3, 3, 4, 4, 4, 4, 3, 3],
            [3, 3, 4, 4, 4, 4, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3],
]


pawnScores = [
            [9, 9, 9, 9, 9, 9, 9, 9],
            [7, 7, 7, 7, 7, 7, 7, 7],
            [3, 3, 3, 3, 3, 3, 3, 3],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [2, 1, 2, 2, 2, 2, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 1, 1, 1, 1, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 0],
]

pieceMatrixList = {'K': kingScores, 'Q': queenScores, 'R': rookScores, 'B': bishopScores, 'N': knightScores, 'p': pawnScores}



CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

'''
Finds a random move
'''

def findRandomMove(validMoves):
   return validMoves[random.randint(0, len(validMoves) - 1)]

'''
Some better algorithm
'''

def findGreedytMove(gs, validMoves):
   turnMultiplier = 1 if gs.whiteToMove else -1
   bestPlayerMove = None
   opponentMinMaxScore = CHECKMATE
   random.shuffle(validMoves)

   for i in range(len(validMoves) - 1, -1, -1):
      playerMove = validMoves[i]
      gs.makeMove(playerMove)
      opponentsMaxScore = -CHECKMATE
      opponentsMoves = gs.getValidMoves()
      playerMoveIsCheck = gs.inCheck
      random.shuffle(opponentsMoves)
      if gs.checkMate:
         opponentMinMaxScore = -CHECKMATE
         bestPlayerMove = playerMove
      if gs.staleMate:
         opponentsMaxScore = 0
      if not gs.checkMate:
         for opponentMove in opponentsMoves:
            gs.makeMove(opponentMove)
            gs.getValidMoves()
            if gs.checkMate:
               opponentsMaxScore = CHECKMATE
            elif gs.staleMate:
               opponentsMaxScore = STALEMATE
            if not gs.checkMate:
               score = -turnMultiplier * scoreMaterial(gs.board)
               if playerMoveIsCheck:
                  score -= 0.5
               if gs.inCheck:
                  score += 1
               if score > opponentsMaxScore:
                  opponentsMaxScore = score
            gs.undoMove()
      if opponentsMaxScore < opponentMinMaxScore:
         opponentMinMaxScore = opponentsMaxScore
         bestPlayerMove = playerMove
      gs.undoMove()
   return bestPlayerMove


'''
Helper method to make the first recursive call
'''
def findBestMoveMinMax(gs, validMoves):
   global nextMove
   nextMove = None
   findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
   return nextMove

'''
Recursive minMax algorithm
'''
def findMoveMinMax(gs, validMoves, depth, whiteToMove):
   global nextMove
   if depth == 0:
      return scoreBoard(gs)

   if whiteToMove:
       maxScore = -CHECKMATE
       for move in validMoves:
           gs.makeMove(move)
           nextMoves = gs.getValidMoves()
           score = findMoveMinMax(gs, nextMoves,depth - 1, False)
           if score > maxScore:
               maxScore = score
               if depth == DEPTH:
                   nextMove = move
           gs.undoMove()
       return maxScore
   else:
       minScore = CHECKMATE
       for move in validMoves:
           gs.makeMove(move)
           nextMoves = gs.getValidMoves()
           score = findMoveMinMax(gs, nextMoves, depth - 1, True)
           if score < minScore:
               minScore = score
               if depth == DEPTH:
                   nextMove = move
           gs.undoMove()
       return minScore


'''
Helper method to make the first recursive call
'''
def findBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None
    counter = 0
    moveOrder = reorderValidMoves(gs, validMoves, 1)
    # for i in range(2, DEPTH + 1):
    #     moveOrder = reorderValidMoves(gs, validMoves, i, moveOrder)
    # nextMove = validMoves[moveOrder[0]]
    # random.shuffle(validMoves)
    turnMultiplier = 1 if gs.whiteToMove else -1
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, turnMultiplier, -CHECKMATE, CHECKMATE, moveOrder)
    # findMoveNegaMax(gs, validMoves, DEPTH, turnMultiplier)
    print(counter)
    return nextMove

'''
Look for maximum score value and multiply by turnMultiplier to account for turn
'''
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves: #make for for player
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        # print(move.getChessNotation(), score)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


'''
Look for maximum score value and multiply by turnMultiplier to account for turn.
Include Alpha Beta pruning.
'''
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, turnMultiplier, alpha, beta, moveOrder = None):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    #should evaluate move ordering to make alg more efficient
    maxScore = -CHECKMATE
    if moveOrder is None:
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -turnMultiplier, -beta, -alpha)
            # print(move.getChessNotation(), score)
            if depth == DEPTH:
                print(move.getChessNotation(), score)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break
    else:
        for i in moveOrder:
            gs.makeMove(validMoves[i])
            nextMoves = gs.getValidMoves()
            score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -turnMultiplier, -beta, -alpha)
            # print(move.getChessNotation(), score)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = validMoves[i]
            gs.undoMove()
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break
    return maxScore



def scoreMovesNegaMaxAlphaBeta(gs, validMoves, depth, turnMultiplier, alpha, beta):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    #should evaluate move ordering to make alg more efficient
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -turnMultiplier, -beta, -alpha)
        # print(move.getChessNotation(), score)
        if score > maxScore:
            maxScore = score
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

'''
Get move order for best moves
'''
def reorderValidMoves(gs, validMoves, depth, sorted_positions_prior = None):
    positions = [None] * len(validMoves)
    scores = [None] * len(validMoves)
    turnMultiplier = 1 if gs.whiteToMove else -1
    if sorted_positions_prior is None:
        for i in range(0, len(validMoves)):
            positions[i] = i
            gs.makeMove(validMoves[i])
            nextMoves = gs.getValidMoves()
            scores[i] = scoreMovesNegaMaxAlphaBeta(gs, nextMoves, depth, -turnMultiplier, -CHECKMATE, CHECKMATE)
            gs.undoMove()
    else:
        for i in sorted_positions_prior:
            positions[i] = i
            gs.makeMove(validMoves[i])
            nextMoves = gs.getValidMoves()
            scores[i] = scoreMovesNegaMaxAlphaBeta(gs, nextMoves, depth, -turnMultiplier, -CHECKMATE, CHECKMATE)
            gs.undoMove()
    combined_lists = zip(scores, positions)
    sorted_combined = sorted(combined_lists)
    sorted_positions = [element for _, element in sorted_combined]

    for value in sorted_positions:
        print(validMoves[value].getChessNotation(), scores[value])

    return sorted_positions

'''
Positive score is good for white, bad for black
'''
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE #black wins
        else:
            return CHECKMATE #white wins
    elif gs.staleMate:
        return STALEMATE # draw
    score = scoreMaterial(gs.board)
    return score


'''
Score the board based on material.
'''
def scoreMaterial(board):
   score = 0
   for row in range(0,8):
      for col in range(0,8):
         if board[row][col][0] == 'w':
            scoreBoard = pieceMatrixList[board[row][col][1]]
            score += scoreBoard[row][col]
            # score += pieceScores[board[row][col][1]]
         elif board[row][col][0] == 'b':
            scoreBoard = pieceMatrixList[board[row][col][1]]
            score -= scoreBoard[7 - row][col]
            # score -= pieceScores[board[row][col][1]]
   return score