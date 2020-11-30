# tp0
# David Shao

from cmu_112_graphics import *
from abc import ABC, abstractmethod
import time


# Some of this code is not working yet...just a general template

class Piece(ABC):
    def __init__(self,row,col,name,color):
        self.row = row
        self.col = col
        self.name = name
        self.color = color
    
    # abstract method for a legal move. A legal move varies from piece to piece.
    @abstractmethod
    def isLegalMove(self,app,newRow,newCol):
        return False
    
    def movePiece(self, app, newRow, newCol):
        if newRow == self.row and newCol == self.col:
            return False
        if 0 <= newRow < 8 and 0 <= newCol <= 8 and self.isLegalMove(app, newRow, newCol):
            targetPiece = getPieceAtPosition(app, newRow, newCol)
            if targetPiece:
                if targetPiece.color == self.color:
                    return False 
                else:
                    app.pieces.remove(targetPiece)
            self.row = newRow
            self.col = newCol
            print(f'New Position: {newRow}, {newCol}')
            return True
        return False

class Bishop(Piece):
    def isLegalMove(self,app,newRow,newCol):
        if abs(self.row - newRow) == abs(self.col - newCol):
            dir = ((newRow - self.row) // abs(newRow - self.row), (newCol - self.col) // abs(newCol - self.col))
            for i in range(1, (newRow - self.row) // dir[0]):
                row = self.row + i * dir[0]
                col = self.col + i * dir[1]
                if getPieceAtPosition(app, row, col):
                    return False
            return True
        return False



class Pawn(Piece):
    def isLegalMove(self, app, newRow, newCol):
        if self.row == 6 and self.row - newRow == 2 and self.col == newCol:
            for i in range(self.row - 1 ,newRow,-1):
                for piece in app.pieces:
                    if piece.row == i and piece.col == self.col:
                        print(piece.name)
                        return False
            return True
        
        elif self.row - newRow == 1 and abs(newCol - self.col) == 1:
            for piece in app.pieces:
                if self.color != piece.color and newRow == piece.row and newCol == piece.col:
                    return True
            return False
        
        elif self.row - newRow == 1 and newCol == self.col:
            for piece in app.pieces:
                if piece.row == newRow and piece.col == newCol:
                    return False
            return True
        return False

class Knight(Piece):
    def isLegalMove(self,app,newRow,newCol):
        if (abs(self.row - newRow) == 1 and abs(self.col - newCol) == 2) or (abs(self.row - newRow) == 2 and abs(self.col - newCol) == 1):
            return True
        return False
                   
        
class Rook(Piece):
    def isLegalMove(self,app,newRow,newCol):
        # check if there is a piece at the new postion.
        # if same color, return False
        targetPiece = getPieceAtPosition(app, newRow, newCol)
        if targetPiece and targetPiece.color == self.color:
            return False
        if self.row == newRow:
            if self.col < newCol:
                for i in range(self.col + 1, newCol):
                    if getPieceAtPosition(app, self.row, i):
                        return False
                return True
            if self.col > newCol:
                for i in range(newCol + 1, self.col):
                    if getPieceAtPosition(app, self.row, i):
                        return False
                return True
        
        if self.col == newCol:
            if self.row < newRow:
                for i in range(self.row + 1, newRow):
                    if getPieceAtPosition(app, i, self.col):
                        return False
                return True
            if self.row > newRow:
                for i in range(self.row + 1, newRow):
                    if getPieceAtPosition(app, i, self.col):
                        return False
                return True

        return False     
                  

class King(Piece):
    def isLegalMove(self,app,newRow,newCol):
        return False

class Queen(Piece):
    def isLegalMove(self,app,newRow,newCol):
        if abs(self.row - newRow) == abs(self.col - newCol):
            dir = ((newRow - self.row) // abs(newRow - self.row), (newCol - self.col) // abs(newCol - self.col))
            for i in range(1, (newRow - self.row) // dir[0]):
                row = self.row + i * dir[0]
                col = self.col + i * dir[1]
                if getPieceAtPosition(app, row, col):
                    return False
            return True
       

        targetPiece = getPieceAtPosition(app, newRow, newCol)
        if targetPiece and targetPiece.color == self.color:
            return False
        if self.row == newRow:
            if self.col < newCol:
                for i in range(self.col + 1, newCol):
                    if getPieceAtPosition(app, self.row, i):
                        return False
                return True
            if self.col > newCol:
                for i in range(newCol + 1, self.col):
                    if getPieceAtPosition(app, self.row, i):
                        return False
                return True
        
        if self.col == newCol:
            if self.row < newRow:
                for i in range(self.row + 1, newRow):
                    if getPieceAtPosition(app, i, self.col):
                        return False
                return True
            if self.row > newRow:
                for i in range(self.row + 1, newRow):
                    if getPieceAtPosition(app, i, self.col):
                        return False
                return True

        return False     
        


def appStarted(app):
    app.whiteTurn = True
    app.moves = []
    app.board = []
    app.pieces = []
    app.canCastle = True 
    # When a piece is clicked, an outline will be drawn around the piece
    app.outlineRow = None
    app.outlineCol = None
    app.selectedPiece = None

    app.pawns = ['Pawn','Pawn','Pawn','Pawn','Pawn','Pawn','Pawn','Pawn']
    app.rows = 8
    app.cols = 8
    app.cellSize = app.height // app.rows
    app.startGrey = True
    initializeBoard(app)
    initializePieces(app)
    
def initializeBoard(app):
    # initializes the board without pieces and with alternating color scheme
    for rows in range(app.rows):
        row = []
        if rows % 2 == 0:
            app.startGrey = True
        else:
            app.startGrey = False
            
        for cols in range(app.cols):
            row.append(app.startGrey)
            app.startGrey = not app.startGrey
        app.board.append(row)

def initializePieces(app):
    # Rook
    app.pieces.append(Rook(0,0,'Rook','Black'))
    app.pieces.append(Rook(0,7,'Rook','Black'))
    app.pieces.append(Rook(7,0,'Rook','White'))
    app.pieces.append(Rook(7,7,'Rook','White'))

    # Knight
    app.pieces.append(Knight(0,1,'Knight','Black'))
    app.pieces.append(Knight(0,6,'Knight','Black'))
    app.pieces.append(Knight(7,1,'Knight','White'))
    app.pieces.append(Knight(7,6,'Knight','White'))

    # Bishop
    app.pieces.append(Bishop(0,2,'Bishop','Black'))
    app.pieces.append(Bishop(0,5,'Bishop','Black'))
    app.pieces.append(Bishop(7,2,'Bishop','White'))
    app.pieces.append(Bishop(7,5,'Bishop','White'))

    # King
    app.pieces.append(King(0,3,'King','Black'))
    app.pieces.append(King(7,3,'King','White'))

    # Queen
    app.pieces.append(Queen(0,4,'Queen','Black'))
    app.pieces.append(Queen(7,4,'Queen','White'))

    
    # All the pawns
    for piece in range(len(app.pawns)):
        # app.pieces.append((app.secondLevel[piece],1,piece,'black'))
        # app.WhitePieces.append((app.secondLevel[piece],len(app.board) - 1 - 1,piece,'white'))
        app.pieces.append(Pawn(1,piece,"Pawn","Black"))
        app.pieces.append(Pawn(len(app.board) - 1 - 1,piece,"Pawn","White"))

def drawPieces(app,canvas):
    for piece in app.pieces:
        x0,y0,x1,y1 = getCellBounds(app,piece.row,piece.col)
        midx = (x0 + x1) // 2
        midy = (y0 + y1) // 2
        canvas.create_text(midx, midy, text = piece.name, fill = piece.color)
    
    
# every time player makes a move, the board and pieces must flip

def flipBoard(app):
    tempBoard = []
    for row in range(len(app.board)):
        tempRow = []
        for col in range(len(app.board[0])):
            tempRow.append(None)
        tempBoard.append(tempRow)
    
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            tempBoard[row][col] = app.board[len(app.board) - 1 - row][col]
    app.board = tempBoard
    app.outlineRow = len(app.board) - 1 - app.outlineRow
    
def flipPieces(app):
    for piece in app.pieces:
       piece.row = len(app.board) - piece.row - 1

def keyPressed(app, event):  
    if (event.key == 'f'):
        flipBoard(app)
        flipPieces(app)

def getPieceAtPosition(app, row, col):
    for piece in app.pieces:
        if piece.row == row and piece.col == col:
            return piece
    return None

def mousePressed(app, event):
    row,col = getCell(app, event.x, event.y)
    app.outlineRow = row
    app.outlineCol = col
    if app.selectedPiece:
        if (app.whiteTurn and app.selectedPiece.color == 'White') or (not app.whiteTurn and app.selectedPiece.color == 'Black'):
            if app.selectedPiece.movePiece(app,row,col):
                flipBoard(app)
                flipPieces(app)
                app.whiteTurn = not app.whiteTurn
                return
                        
    app.selectedPiece = getPieceAtPosition(app, row, col)

   

#similar to getCell from lecture, just without margins
def getCell(app, x, y):
    return int(y/app.cellSize), int(x/app.cellSize)

def drawBoard(app,canvas):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            x0,y0,x1,y1 = getCellBounds(app,row,col)
            if app.board[row][col]:
                color = 'grey'
            else:
                color = 'green'
            if (app.outlineRow or app.outlineCol != None) and (row,col) == (app.outlineRow, app.outlineCol):
                canvas.create_rectangle(x0,y0,x1-1,y1-1,fill = color, outline = 'yellow')
            else:
                canvas.create_rectangle(x0,y0,x1,y1,fill = color, outline = '') 
               

def redrawAll(app,canvas):
    drawBoard(app,canvas)
    drawPieces(app,canvas)

def getCellBounds(app,row,col):
    x0 = col * app.cellSize
    y0 = row * app.cellSize
    x1 = x0 + app.cellSize
    y1 = y0 + app.cellSize
    return (x0, y0, x1, y1)

def main():
    runApp(width=1024, height=768)
    

if __name__ == '__main__':
    main()
    



            






