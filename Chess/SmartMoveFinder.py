import random

pieceScores = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
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
   for playerMove in validMoves:
      gs.makeMove(playerMove)
      opponentsMoves = gs.getValidMoves()
      opponentsMaxScore = -CHECKMATE
      for opponentMove in opponentsMoves:
         gs.makeMove(opponentMove)
         if gs.checkMate:
            opponentsMaxScore = -CHECKMATE
         elif gs.staleMate:
            opponentsMaxScore = STALEMATE
         else:
            score = -turnMultiplier * scoreMaterial(gs.board)
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

def scoreMaterial(board):
   score = 0
   for row in board:
      for square in row:
         if square[0] == 'w':
            score += pieceScores[square[1]]
         elif square[0] == 'b':
            score -= pieceScores[square[1]]
   return score