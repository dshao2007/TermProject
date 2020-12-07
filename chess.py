# tp0
# David Shao

from cmu_112_graphics import *
from abc import ABC, abstractmethod
import time
import copy
import sys

boardSize = 8

class Piece(ABC):
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

    def __str__(self):
        return self.getShortName()

    @abstractmethod
    def isLegalMove(self, game, newRow, newCol):
        ''' check if it is leagal to move to the new position.
            A legal move varies from piece to piece, to be implemented
            in the subclasses.
        Args:
         game: the ChessGame object. This is use to query the piece at
            a position.
         newRow, newCol: the new position to move to.
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

class Knight(Piece):
    def isLegalMove(self,game,newRow,newCol):
        if (abs(self.row - newRow) == 1 and abs(self.col - newCol) == 2) or (abs(self.row - newRow) == 2 and abs(self.col - newCol) == 1):
            return True
        return False


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
            piece.move(self.row, newCol)


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
            piece.move(self.row, newCol, True)
            piece.numMoves = 0

        
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


class ChessGame(object):

    def __init__(self):
        self.pieces = []

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


        # Rook
        self.pieces.append(Rook(0, 0, 'Rook', 'Black'))
        self.pieces.append(Rook(0, 7, 'Rook', 'Black'))
        self.pieces.append(Rook(7, 0, 'Rook', 'White'))
        self.pieces.append(Rook(7, 7, 'Rook', 'White'))

        # Queen
        self.pieces.append(Queen(0, 3, 'Queen', 'Black'))
        self.pieces.append(Queen(7, 3, 'Queen', 'White'))        


        # King
        self.pieces.append(King(0, 4, 'King', 'Black'))
        self.pieces.append(King(7, 4, 'King', 'White'))

        for piece in self.pieces:
            self.board[(piece.row, piece.col)] = piece

    def getPieces(self):
        return self.pieces
    
    # Assumes movement passes all the prelimianry rules and changes the game state
    def makeMove(self,piece,newRow,newCol,targetPiece):
        
        if targetPiece:
            self.pieces.remove(targetPiece)
            self.captured.append(targetPiece)
        self.moves.append((piece, piece.row, piece.col,

        oldRow, oldCol = piece.getPosition()
        piece.move(newRow,newCol)

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
            return
        
        piece, oldRow, oldCol, row, col, hasCapture = self.moves.pop()
        if oldRow == row and oldCol == col:
            # turn the queen to pawn
            self.undoPromote(piece, self.captured.pop())
            return

        if hasCapture:
            targetPeice = self.captured.pop()
            self.pieces.append(targetPeice)
        piece.move(oldRow, oldCol, isUndo=True)
        if piece.name == 'King' and abs(oldCol - col) == 2:
            piece.handleCastleRookUndo(self, col)

    def undoPromote(self, queen, pawn):
        self.pieces.remove(queen)
        self.pieces.append(pawn)
        # undo the Pawn's move before promoting to Queen
        self.undoLastMove()


    def inCheck(self, color):
        ''' check if the specified player is in check '''
        kingRow, kingCol = self.kingPosition(color)
        for piece in self.pieces:
            if piece.color != color and piece.isLegalMove(self, kingRow, kingCol):
                return True
        return False


    def checkMate(self, color):
        ''' Check if player with given color is in checkmate by the other player
        returns True if it is in checkMate, false otherwise
        precondition: the player is in check
        '''
        assert self.inCheck(color), "expect inCheck position"
        moves = self.getAllLegalMoves(color)
        # print(moves)
        return len(moves) == 0


    def printMoves(self):
        print("moving of the game")
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
        
        # A special move: pawn to Queen promotion, row and col unchanged
        self.moves.append((queen, row, col, row, col, True))
    

    def movePiece(self, piece, newRow, newCol, aiMode=False, simulate=False):
        ''' Move a piece to the new position '''
        tempRow, tempCol = piece.getPosition()
        
        if newRow == tempRow and newCol == tempCol:
            return False

        # need to be in the range
        if newRow >= boardSize or newRow < 0 or newCol < 0 or newCol >= boardSize:
            return False

        # check if the move is legal for the piece
        if not piece.isLegalMove(self, newRow, newCol):
            return False
        
        # get the piece, if any, at the new position
        targetPiece = self.getPieceAtPosition(newRow, newCol)
        if targetPiece:
            # cannot move if the target piece has same color
            if targetPiece.color == piece.color:
                return False
        # As of now, we are good to make a move. 
        # Move the piece to the new position
        self.makeMove(piece,newRow,newCol,targetPiece)
                
        # undo the tentative move if that would result in check.
        if self.inCheck(piece.color):
            # undo the capture if a capture would have happened
            self.undoLastMove()
            return False

        # Now, we have made the move, but we still undo if it is a simulation.
        # We don't want the simulated move to show up in the actual game.
        if simulate:
            self.undoLastMove()
            return True   

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
    

    def getAllLegalMoves(self,color):
        legalMoves = []
        for piece in self.pieces:
            if piece.color == color:
                for row in range(boardSize):
                    for col in range(boardSize):
                        if self.movePiece(piece, row, col, aiMode=False, simulate=True):
                            legalMoves.append((piece,row,col))
                            
        return legalMoves



