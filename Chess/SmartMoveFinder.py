import random

pieceScores = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
kingScores = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 0, 0, 1, 1, 1]
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
            [4, 4, 4, 4, 4, 4, 4, 4]
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
            [3, 3, 3, 3, 3, 3, 3, 3],
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


'''
Finds a random move
'''

def findRandomMove(validMoves):
   return validMoves[random.randint(0, len(validMoves) - 1)]

'''
Some better algorithm
'''

def findBestMove(gs, validMoves):
   turnMultiplier = 1 if gs.whiteToMove else -1
   bestPlayerMove = findRandomMove(validMoves)
   opponentMinMaxScore = CHECKMATE
   random.shuffle(validMoves)
   for playerMove in validMoves:
      gs.makeMove(playerMove)
      if gs.checkMate:
         opponentMinMaxScore = -CHECKMATE
         bestPlayerMove = playerMove
      if gs.staleMate:
         opponentsMaxScore = 0
      else:
         opponentsMoves = gs.getValidMoves()
         opponentsMaxScore = -CHECKMATE
         for opponentMove in opponentsMoves:
            gs.makeMove(opponentMove)
            gs.getValidMoves()
            if gs.checkMate:
               opponentsMaxScore = -turnMultiplier * CHECKMATE
            elif gs.staleMate:
               opponentsMaxScore = STALEMATE
            else:
               score = -turnMultiplier * scoreMaterial(gs, gs.board)
               if score > opponentsMaxScore:
                  opponentsMaxScore = score
            gs.undoMove()
      if opponentsMaxScore < opponentMinMaxScore:
         opponentMinMaxScore = opponentsMaxScore
         bestPlayerMove = playerMove
      gs.undoMove()
   return bestPlayerMove


'''
Score the board based on material.
'''

def scoreMaterial(gs, board):
   score = 0
   for row in range(0,7):
      for col in range(0,7):
         if board[row][col][0] == 'w':
            # scoreBoard = pieceScores[board[row][col][1]]
            score += pieceScores[board[row][col][1]]
         elif board[row][col][0] == 'b':
            # scoreBoard = pieceMatrixList[board[row][col][1]]
            score -= pieceScores[board[row][col][1]]
   return score