# tp0
# David Shao

from cmu_112_graphics import *
from abc import ABC, abstractmethod
import time
import copy
import sys

boardSize = 8

class Piece(ABC):
    POINTS = {'Pawn': 10, 'Knight': 30, 'Bishop': 30,
              'Rook': 50, 'Queen': 90, 'King': 200} 
    def __init__(self, row, col, name, color):
        self.row = row
        self.col = col
        self.name = name
        self.color = color
        self.numMoves = 0

    def getPosition(self):
        return (self.row, self.col)

    def getShortName(self):
        return self.color + self.name

    def getOpponentColor(self):
        return 'Black' if self.color == 'White' else 'White'

    @abstractmethod
    def getPossibleMoves(self):
        '''
        All pieces have possible moves, but it differs from piece to piece. 
        Only checks possible moves without regard to other pieces
        '''
        return []

    def getLegalMoves(self, game, fullValidate=True):
        moves = []
        
        for row, col in self.getPossibleMoves():
            if self.isLegalMove(game, row, col):
                value = 0
                piece = game.getPieceAtPosition(row, col)
                if piece:
                    if piece.color == self.color:
                        continue
                    else:
                        value = self.POINTS[piece.name]
                if fullValidate:
                    if game.validateMove(self, row, col):
                        moves.append((self, row, col, value))        
                else:
                    moves.append((self, row, col, value))           
        return moves
    
    def __str__(self):
        return self.getShortName() + f"{self.row}-{self.col}"

    def __repr__(self):
        return self.getShortName() + f"{self.row}-{self.col}"

    @abstractmethod
    def isLegalMove(self, game, newRow, newCol):
        ''' check if it is legal to move to the new position.
            A legal move varies from piece to piece, to be implemented
            in the subclasses.
        '''
        return False

    def move(self, newRow, newCol, isUndo=False):
        ''' Move to a new position. This is called by the game object. '''
        self.row = newRow
        self.col = newCol
        if isUndo:
            self.numMoves -= 1
        else:
            self.numMoves += 1

    def getDiagonalMoves(self, limit=7):
        moves = []
        
        row = self.row
        col = self.col
        for i in range(1, limit+1):
            if row+i < 8 and col+i < 8:
                moves.append((row+i, col+i))
            if row-i >= 0 and col-i >= 0:
                moves.append((row-i, col-i))
            if row+i < 8 and col-i >=0:
                moves.append((row+i, col-i))
            if row-i >= 0 and col+i <8:
                moves.append((row-i, col+i))
        return moves

    def getLineMoves(self, limit=7):
        moves = []
        
        row = self.row
        col = self.col
        for i in range(1, limit+1):
            if row+i < 8:
                moves.append((row+i, col))
            if row-i >= 0:
                moves.append((row-i, col))
            if col-i >=0:
                moves.append((row, col-i))
            if col+i <8:
                moves.append((row, col+i))
        return moves

class Bishop(Piece):
    def isLegalMove(self,game,newRow,newCol):
        if abs(self.row - newRow) == abs(self.col - newCol):
            dir = ((newRow - self.row) // abs(newRow - self.row), (newCol - self.col) // abs(newCol - self.col))
            for i in range(1, (newRow - self.row) // dir[0]):
                row = self.row + i * dir[0]
                col = self.col + i * dir[1]
                if game.getPieceAtPosition(row, col):
                    return False
            return True
        return False

    def getPossibleMoves(self):
        return self.getDiagonalMoves()
        
class Pawn(Piece):
    def isLegalMove(self, game, newRow, newCol):
        if self.color == 'White':
            return self.checkWhite(game, newRow, newCol)
        else:
            return self.checkBlack(game, newRow, newCol)
    
    def checkForPromotion(self):
        return (self.color == 'White' and self.row == 0) or (self.color == 'Black' and self.row == 7)
    
    def checkWhite(self, game, newRow, newCol):
        if (self.row == 6 and self.row - newRow == 2) and self.col == newCol:
            for i in range(newRow, self.row):
                for piece in game.pieces:
                    if piece.row == i and piece.col == self.col:
                        # print(piece.name)
                        return False
            return True
        elif self.row - newRow == 1 and abs(newCol - self.col) == 1:
            for piece in game.pieces:
                if self.color != piece.color and newRow == piece.row and newCol == piece.col:
                    return True
            return False
        elif self.row - newRow == 1 and newCol == self.col:
            for piece in game.pieces:
                if piece.row == newRow and piece.col == newCol:
                    return False
            return True
        return False
    
    def checkBlack(self, game, newRow, newCol):
        if (self.row == 1 and self.row - newRow == -2) and self.col == newCol:
            for i in range(self.row + 1,newRow+1):
                for piece in game.pieces:
                    if piece.row == i and piece.col == self.col:
                        # print(piece.name)
                        return False
            return True
        elif self.row - newRow == -1 and abs(newCol - self.col) == 1:
            for piece in game.pieces:
                if self.color != piece.color and newRow == piece.row and newCol == piece.col:
                    return True
            return False
        elif self.row - newRow == -1 and newCol == self.col:
            for piece in game.pieces:
                if piece.row == newRow and piece.col == newCol:
                    return False
            return True
        return False

    def getPossibleMoves(self):
        # may contain illegal moves.
        return self.getLineMoves(2) + self.getDiagonalMoves(1)

class Knight(Piece):
    def isLegalMove(self,game,newRow,newCol):
        if (abs(self.row - newRow) == 1 and abs(self.col - newCol) == 2) or (abs(self.row - newRow) == 2 and abs(self.col - newCol) == 1):
            return True
        return False

    def getPossibleMoves(self):
        # may contain illegal moves.
        moves=[]
        row = self.row
        col = self.col
        delta = [(-1,2),(1,2),(-1,-2),(1,-2),(-1,2),
                 (2,-1),(2,1),(-2,-1),(-2,1),(2,-1)]
        for d in delta:
            if row+d[0] < 8 and row+d[0] >=0 and col+d[1] < 8 and col+d[1] >=0:
                moves.append((row+d[0], col+d[1]))
        return moves
    
class Rook(Piece):
    def isLegalMove(self,game,newRow,newCol):
        # check if there is a piece at the new postion.
        # if same color, return False
        targetPiece = game.getPieceAtPosition(newRow, newCol)
        if targetPiece and targetPiece.color == self.color:
            return False
        if self.row == newRow:
            if self.col < newCol:
                for i in range(self.col + 1, newCol):
                    if game.getPieceAtPosition(self.row, i):
                        return False
                return True
            if self.col > newCol:
                for i in range(newCol + 1, self.col):
                    if game.getPieceAtPosition(self.row, i):
                        return False
                return True

        if self.col == newCol:
            if self.row < newRow:
                for i in range(self.row + 1, newRow):
                    if game.getPieceAtPosition(i, self.col):
                        return False
                return True
            if self.row > newRow:
                for i in range(newRow + 1, self.row):
                    if game.getPieceAtPosition(i, self.col):
                        return False
                return True

        return False

    def getPossibleMoves(self):
        # may contain illegal moves.
        return self.getLineMoves(8)
    
class King(Piece):
    def isLegalMove(self,game,newRow,newCol):
        if  abs(self.row - newRow) <= 1 and abs(self.col - newCol) <= 1:
            return True

        if self.numMoves > 0:
            return False

        # Castle
        if self.row != newRow:
            return False
        
        if self.color == 'White':
            castleRow = 7
        else:
            castleRow = 0

        if newCol == 2:
            rookCol = 0
            noPiece = [1, 2, 3]
            checkCol = 3
        elif newCol == 6:
            rookCol = 7
            noPiece = [5, 6]
            checkCol = 5
        else:
            return False
            
        if newRow == castleRow:
            # make sure there are no game pieces in between
            for col in noPiece:
                if game.getPieceAtPosition(castleRow, col) is not None:
                    return False
    
            # make sure King is not under Check
            
            # chcek if the current King position is in check
            if game.inCheck(self.color):
                return False

            # check in-flight and final position are not in Check
            for piece in game.pieces:
                if piece.color != self.color and piece.isLegalMove(game, castleRow, checkCol):
                    return False
                # not under Check, when King is moved to the new location (self.row, newCol)
                if piece.color != self.color and piece.isLegalMove(game, castleRow, newCol):
                    return False

            # find the Rook to move
            piece = game.getPieceAtPosition(castleRow, rookCol)
            if piece is None:
                return False
            if piece.name == 'Rook' and piece.numMoves == 0 and piece.color == self.color:
                return True

        return False

    # called after the King made a castle move
    def handleCastleRookMove(self,game,oldCol):
        # print("handle Castle Rook Move ", oldCol)
        if self.col == 2:
            col = 0
            newCol = 3
        elif self.col == 6:
            col = 7
            newCol = 5
        else:
            assert False, "not a castle move"

        piece = game.getPieceAtPosition(self.row, col)
        if piece:
            del game.board[piece.getPosition()]
            piece.move(self.row, newCol)
            game.board[(self.row, newCol)] = piece

    # called after the King made a castle move
    def handleCastleRookUndo(self,game,oldKingCol):
        #print("handle Castle Rook Undo ", oldKingCol)

        # this would be an undo of the castle
        if oldKingCol == 2:
            col = 3 # rook at col=3, move to 0 to undo
            newCol = 0
        elif oldKingCol == 6:
            col = 5 # rook at col=5, move to 7
            newCol = 7
        else:
            assert False, "not a castle move"

        piece = game.getPieceAtPosition(self.row, col)
        if piece:
            del game.board[piece.getPosition()]
            piece.move(self.row, newCol, True)
            game.board[(self.row, newCol)] = piece
            piece.numMoves = 0

    def getPossibleMoves(self):
        # may contain illegal moves.
        return self.getLineMoves(2) + self.getDiagonalMoves(1)
        
class Queen(Piece):
    def isLegalMove(self,game,newRow,newCol):
        # same as Bishop
        if abs(self.row - newRow) == abs(self.col - newCol):
            dir = ((newRow - self.row) // abs(newRow - self.row),
             (newCol - self.col) // abs(newCol - self.col))
            for i in range(1, (newRow - self.row) // dir[0]):
                row = self.row + i * dir[0]
                col = self.col + i * dir[1]
                if game.getPieceAtPosition(row, col):
                    return False
            return True

        # same as Rook
        targetPiece = game.getPieceAtPosition(newRow, newCol)
        if targetPiece and targetPiece.color == self.color:
            return False
        if self.row == newRow:
            if self.col < newCol:
                for i in range(self.col + 1, newCol):
                    if game.getPieceAtPosition(self.row, i):
                        return False
                return True
            if self.col > newCol:
                for i in range(newCol + 1, self.col):
                    if game.getPieceAtPosition(self.row, i):
                        return False
                return True

        if self.col == newCol:
            if self.row < newRow:
                for i in range(self.row + 1, newRow):
                    if game.getPieceAtPosition(i, self.col):
                        return False
                return True
            if self.row > newRow:
                for i in range(newRow + 1, self.row):
                    if game.getPieceAtPosition(i, self.col):
                        return False
                return True

        return False

    def getPossibleMoves(self):
        # may contain illegal moves.
        return self.getLineMoves() + self.getDiagonalMoves()
    
class ChessGame(object):

    def __init__(self):
        self.pieces = []
        self.blackPieces = []
        self.whitePieces = []
        # record all the moves
        self.moves = []
        self.board = {}
        # captured pieces
        self.captured = []
        self.gameOver = False
        
        self.initializePieces()

   
    def initializePieces(self):
        # All the pawns
        for piece in range(boardSize):
            self.pieces.append(Pawn(1, piece, "Pawn", "Black"))
            self.pieces.append(Pawn(boardSize - 1 - 1, piece, "Pawn", "White"))

        # Bishop
        self.pieces.append(Bishop(0, 2, 'Bishop', 'Black'))
        self.pieces.append(Bishop(0, 5, 'Bishop', 'Black'))
        self.pieces.append(Bishop(7, 2, 'Bishop', 'White'))
        self.pieces.append(Bishop(7, 5, 'Bishop', 'White'))

        # Knight
        self.pieces.append(Knight(0, 1, 'Knight', 'Black'))
        self.pieces.append(Knight(0, 6, 'Knight', 'Black'))
        self.pieces.append(Knight(7, 1, 'Knight', 'White'))
        self.pieces.append(Knight(7, 6, 'Knight', 'White'))
        # Queen
        self.pieces.append(Queen(0, 3, 'Queen', 'Black'))
        self.pieces.append(Queen(7, 3, 'Queen', 'White'))        

        # Rook
        self.pieces.append(Rook(0, 0, 'Rook', 'Black'))
        self.pieces.append(Rook(0, 7, 'Rook', 'Black'))
        self.pieces.append(Rook(7, 0, 'Rook', 'White'))
        self.pieces.append(Rook(7, 7, 'Rook', 'White'))

        # King
        self.pieces.append(King(0, 4, 'King', 'Black'))
        self.pieces.append(King(7, 4, 'King', 'White'))

        self.rebuildBoard()
        
    def getPieces(self):
        return self.pieces

    def rebuildBoard(self):
        for piece in self.pieces:
            self.board[piece.getPosition()] = piece

    # Assumes movement passes all the prelimianry rules and changes the game state
    def makeMove(self,piece,newRow,newCol,targetPiece):
        if targetPiece:
            self.pieces.remove(targetPiece)
            self.captured.append(targetPiece)
        self.moves.append((piece, piece.row, piece.col,
                           newRow, newCol, targetPiece is not None))

        oldRow, oldCol = piece.getPosition()
        piece.move(newRow,newCol)

        del self.board[(oldRow, oldCol)]
        self.board[(newRow,newCol)] = piece
                       
        # if pawn at promotion position, then, promote to queen
        if piece.name == 'Pawn':
            if piece.checkForPromotion():
                self.promotePiece(piece)
        elif piece.name == 'King':
            if abs(oldCol - newCol) == 2:
                piece.handleCastleRookMove(self, oldCol)
                
    
    # Useful for simulations and AI, where we may not want a move to be reflected in a game
    def undoLastMove(self):
        if len(self.moves) == 0:
            print("nothing to undo")
            return False
        
        piece, oldRow, oldCol, row, col, hasCapture = self.moves.pop()
        if oldRow == row and oldCol == col:
            # turn the queen to pawn
            self.undoPromote(piece, self.captured.pop())
            return True

        if hasCapture:
            targetPiece = self.captured.pop()
            self.pieces.append(targetPiece)
            self.board[targetPiece.getPosition()] = targetPiece
        else:
            del self.board[(row, col)]
        piece.move(oldRow, oldCol, isUndo=True)
        self.board[(oldRow, oldCol)] = piece
        if piece.name == 'King' and abs(oldCol - col) == 2:
            piece.handleCastleRookUndo(self, col)

        return True

    def undoPromote(self, queen, pawn):
        self.pieces.remove(queen)
        self.pieces.append(pawn)
        self.board[pawn.getPosition()] = pawn
        # undo the Pawn's move before promoting to Queen
        self.undoLastMove()


    def inCheck(self, color):
        ''' check if the specified player is in check '''
        kingRow, kingCol = self.kingPosition(color)
        for piece in self.pieces:
            if piece.color != color and piece.isLegalMove(self, kingRow, kingCol):
                return True
        return False

    # for loading
    def rebuildFromMoves(self,moves):
        ''' Rebuild the game state from the move and return the color of the last move '''
        color = 'White'
        for move in moves:
            _, oldRow, oldCol, newRow, newCol, _ = move
            piece = self.getPieceAtPosition(oldRow, oldCol)
            self.movePiece(piece, newRow, newCol)
            color = piece.color
        return color


    def checkMate(self, color):
        ''' Check if player with given color is in checkmate by the other player
        returns True if it is in checkMate, false otherwise
        precondition: the player is in check
        '''
        moves = self.getAllLegalMoves(color)
        # print(moves)
        return len(moves) == 0


    def printMoves(self):
        for move in self.moves:
            print(move)

    def promotePiece(self,piece):
        row = piece.row
        col = piece.col
        # only promote to Queen
        queen = Queen(row, col, 'Queen', piece.color)
        self.pieces.remove(piece)
        self.captured.append(piece)
        self.pieces.append(queen)
        self.board[(row, col)] = queen
        
        # A special move: pawn to Queen promotion, row and col unchanged
        self.moves.append((queen, row, col, row, col, True))
    
    def validateMove(self, piece, newRow, newCol):
        tempRow, tempCol = piece.getPosition()
        
        if newRow == tempRow and newCol == tempCol:
            #print("move cannot be the same pos")
            return False

        # need to be in the range
        if newRow >= boardSize or newRow < 0 or newCol < 0 or newCol >= boardSize:
            assert False, "out of rance (0-7)"
            return False

        # check if the move is legal for the piece
        if not piece.isLegalMove(self, newRow, newCol):
            #print(" piece isLegaMove == False")
            return False
        
        # get the piece, if any, at the new position
        targetPiece = self.getPieceAtPosition(newRow, newCol)
        if targetPiece:
            # cannot move if the target piece has same color
            if targetPiece.color == piece.color:
                #print(" piece same color capture not allowed")
                return False
        # As of now, we are good to make a move. 
        # Move the piece to the new position
        self.makeMove(piece,newRow,newCol,targetPiece)
                
        # undo the tentative move if that would result in check.
        if self.inCheck(piece.color):
            # undo the capture if a capture would have happened
            self.undoLastMove()
            # print(" piece move would end with Check")
            return False

        # Now, we have made the move, but we still undo if it is a simulation.
        # We don't want the simulated move to show up in the actual game.
        self.undoLastMove()
        return True   

    def movePieceNoCheck(self,  piece, newRow, newCol, aiMode=False, simulate=False):
        # get the piece, if any, at the new position
        targetPiece = self.getPieceAtPosition(newRow, newCol)
        if targetPiece:
            # cannot move if the target piece has same color
            if targetPiece.color == piece.color:
                print(" piece same color capture not allowed")
                return False
        # As of now, we are good to make a move. 
        # Move the piece to the new position
        self.makeMove(piece,newRow,newCol,targetPiece)
        otherColor = piece.getOpponentColor()
        # after player makes move, it is now the other player's turn.
        # See if other player is in checkmate
        if self.inCheck(otherColor) and not aiMode:
            if not simulate:
                if self.checkMate(otherColor):
                    self.endGame(otherColor)
                    return True
        #print(f'New Position: {newRow}, {newCol}')
        return True

        
    def movePiece(self, piece, newRow, newCol, aiMode=False, simulate=False):
        ''' Move a piece to the new position '''
        tempRow, tempCol = piece.getPosition()
        
        if newRow == tempRow and newCol == tempCol:
            print("move cannot be the same pos")
            return False

        # need to be in the range
        if newRow >= boardSize or newRow < 0 or newCol < 0 or newCol >= boardSize:
            assert False, "out of rance (0-7)"
            return False

        # check if the move is legal for the piece
        if not piece.isLegalMove(self, newRow, newCol):
            print(" piece isLegaMove == False", piece)
            return False
        
        # get the piece, if any, at the new position
        targetPiece = self.getPieceAtPosition(newRow, newCol)
        if targetPiece:
            # cannot move if the target piece has same color
            if targetPiece.color == piece.color:
                print(" piece same color capture not allowed")
                return False
        # As of now, we are good to make a move. 
        # Move the piece to the new position
        self.makeMove(piece,newRow,newCol,targetPiece)
                
        # undo the tentative move if that would result in check.
        if self.inCheck(piece.color):
            # undo the capture if a capture would have happened
            self.undoLastMove()
            # print(" piece move would end with Check")
            return False

        # Now, we have made the move, but we still undo if it is a simulation.
        # We don't want the simulated move to show up in the actual game.
        if simulate:
            self.undoLastMove()
            return True   

        otherColor = piece.getOpponentColor()
        # after player makes move, it is now the other player's turn.
        # See if other player is in checkmate
        if not aiMode and not simulate:
            self.checkForStatus(otherColor)

        #print(f'New Position: {newRow}, {newCol}')
        return True

    # return True if game is over for otherColor
    def checkForStatus(self, otherColor):
        print("checking for checkmate ", otherColor)
        if self.inCheck(otherColor):
            if self.checkMate(otherColor):
                self.endGame(otherColor)
                return True
            else:
                moves=self.getAllLegalMoves(otherColor)
                for move in moves:
                    print(move)
        return False

    def endGame(self,loser):
        self.gameOver = True
        self.loser = loser
        if self.loser == 'White':
            self.winner = 'Black'
        else:
            self.winner = 'White'
                      
    # find out where the king is
    def kingPosition(self,color):
        for piece in self.pieces:
            if piece.color == color and piece.name == 'King':
                kingRow = piece.row
                kingCol = piece.col
                return (kingRow, kingCol)
        return None

    
    def getPieceAtPosition(self, row, col):
        for piece in self.pieces:
            if piece.row == row and piece.col == col:
                return piece
        return None

    def getAllLegalMoves(self,color, fullValidate=True):
        legalMoves = []
        for piece in self.pieces:
            if piece.color == color:
                legalMoves.extend(piece.getLegalMoves(self))
        # prioritze moves that kill a piece or have points
        legalMoves.sort(key=lambda f: f[2], reverse=True)
        return legalMoves



