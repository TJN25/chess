"""
This class is responsible for storing all the information about the current states, the available moves and a move log
"""

class GameState():
    def __init__(self):
        #board is 8 x 8 2d list. Each element of the list has two characters.
        #The first letter represents the colour
        #The second letter represents the piece
        #"--" represents an empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'p' : self.getPawnMoves, 'R' : self.getRookMoves, 'N' : self.getKnightMoves, 'B' : self.getBishopMoves, 'Q' : self.getQueenMoves, 'K' : self.getKingMoves}

        self.whiteToMove = True
        self.movelog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0, 4)

        '''
        Takes a move as a paramter and executes it. This will not work for castling, en passant, and pawn promotion
        '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move) #log the move so that the history can be displayed and undo is possible
        #update the king location
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
        self.whiteToMove = not self.whiteToMove #swap players


    def undoMove(self):
        if len(self.movelog) != 0: #make sure there is a move to undo
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved #put piece back
            self.board[move.endRow][move.endCol] = move.pieceCaptured #put piece back
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            self.whiteToMove = not self.whiteToMove #switch sides


    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves() #for now we will not worry about checks etc.

    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of columns in row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) #calls appropriate move function based on piece types
        return moves

    '''
    get all the piece moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawns to move
            if (r - 1) >= 0 and self.board[r-1][c] == "--": #one square move is empty
                moves.append(Move((r,c),(r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == "--": ##two square move is empty
                    moves.append(Move((r, c),(r - 2, c), self.board))
            if (r-1) >= 0 and (c-1) >= 0 and self.board[r-1][c-1][0] == "b":
                moves.append(Move((r, c), (r-1, c-1), self.board))
            if (r-1) >= 0 and (c+1) <= 7 and self.board[r-1][c+1][0] == "b":
                moves.append(Move((r, c), (r-1, c+1), self.board))
        else:
            if self.board[r+1][c] == "--" and r + 1 <= 7: #one square move is empty
                moves.append(Move((r,c),(r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == "--": ##two square move is empty
                    moves.append(Move((r, c),(r + 2, c), self.board))
            if (r+1) <= 7 and (c-1) >= 0 and self.board[r+1][c-1][0] == "w":
                moves.append(Move((r, c), (r+1, c-1), self.board))
            if (r+1) <= 7 and (c+1) <= 7 and self.board[r+1][c+1][0] == "w":
                moves.append(Move((r, c), (r+1, c+1), self.board))
        #add pawn promotions later
    def getRookMoves(self, r, c, moves):
        directions = ((-1,0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7: #on the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space is valid
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece is valid
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    else: # friendly piece is invalid
                        break
                else: # off the board
                    break
    def getKnightMoves(self, r, c, moves):
        directions = ((1, -2), (1,2), (-1, -2), (-1, 2), (2, -1), (2, 1), (-2, -1), (-2, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:  # on the board
                endPiece = self.board[endRow][endCol]
                if endPiece == "--":  # empty space is valid
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                elif endPiece[0] == enemyColor:  # enemy piece is valid
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (1, -1), (1, 1), (-1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:  # on the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space is valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece is valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    else:  # friendly piece is invalid
                        break
                else:  # off the board
                    break
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (1, -1), (1, 1), (-1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:  # on the board
                endPiece = self.board[endRow][endCol]
                if endPiece == "--":  # empty space is valid
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                elif endPiece[0] == enemyColor:  # enemy piece is valid
                    moves.append(Move((r, c), (endRow, endCol), self.board))


class Move():
    # maps keys to values
    # key : value
    ranksToRows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4,
                   "5" : 3, "6" : 2, "7" : 1, "8" : 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"h" : 7, "g" : 6, "f" : 5, "e" : 4,
                   "d" : 3, "c" : 2, "b" : 1, "a" : 0}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol

    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]