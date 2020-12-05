# tp0
# David Shao

from cmu_112_graphics import *
from abc import ABC, abstractmethod
import time
import copy
import sys
import chess

class MyApp(App):
    def appStarted(self):
        self.whiteTurn = True
        self.moves = []
        self.board = []
        self.chessGame = chess.ChessGame()
        self.canCastle = True
        # When a piece is clicked, an outline will be drawn around the piece
        self.outlineRow = None
        self.outlineCol = None
        self.selectedPiece = None

        self.pawns = ['Pawn','Pawn','Pawn','Pawn','Pawn','Pawn','Pawn','Pawn']
        self.rows = 8
        self.cols = 8
        self.cellSize = self.height // self.rows
        self.startGrey = True
        self.gameOver = False
        self.images = {}
        self.initializeBoard()
        self.initializePieces()

    def initializeBoard(self):
        # initializes the board without pieces and with alternating color scheme
        for rows in range(self.rows):
            row = []
            if rows % 2 == 0:
                self.startGrey = True
            else:
                self.startGrey = False

            for _ in range(self.cols):
                row.append(self.startGrey)
                self.startGrey = not self.startGrey
            self.board.append(row)

    def initializePieces(self):
        self.images['BlackQueen'] = self.loadImage('./images/pieces/bQ.png')
        self.images['BlackPawn'] = self.loadImage('./images/pieces/bP.png')
        self.images['BlackBishop'] = self.loadImage('./images/pieces/bB.png')
        self.images['BlackKnight'] = self.loadImage('./images/pieces/bN.png')
        self.images['BlackRook'] = self.loadImage('./images/pieces/bR.png')
        self.images['BlackKing'] = self.loadImage('./images/pieces/bK.png')

        self.images['WhiteQueen'] = self.loadImage('./images/pieces/wQ.png')
        self.images['WhitePawn'] = self.loadImage('./images/pieces/wP.png')
        self.images['WhiteBishop'] = self.loadImage('./images/pieces/wB.png')
        self.images['WhiteKnight'] = self.loadImage('./images/pieces/wN.png')
        self.images['WhiteRook'] = self.loadImage('./images/pieces/wR.png')
        self.images['WhiteKing'] = self.loadImage('./images/pieces/wK.png')

    def drawCoords(self, canvas):
         if self.whiteTurn:
             for row in range(chess.boardSize):
                 canvas.create_text(8,row * self.cellSize + 15,
                                    text = f'{8 - row}', fill = '#99FFCC')
                 canvas.create_text(self.cellSize - 16 + row * self.cellSize,self.height - 20,
                                    text = chr(ord('a') + row), fill = '#99FFCC')
         else:
             for row in range(len(self.board)):
                 canvas.create_text(self.height - 8,
                                    row * self.cellSize + 15,
                                    text = f'{row + 1}', fill = '#99FFCC')
                 canvas.create_text(16 + row * self.cellSize,
                                    self.height - 20,
                                    text = chr(ord('h') - row),
                                    fill = '#99FFCC')


    def drawPieces(self,canvas):
        for piece in self.chessGame.getPieces():
            x0,y0,x1,y1 = self.getCellBounds(piece.row,piece.col)
            midx = (x0 + x1) // 2
            midy = (y0 + y1) // 2
            imageKey = piece.color + piece.name
            # Image Method from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
            canvas.create_image(midx, midy, image=ImageTk.PhotoImage(self.images[imageKey]))


    # every time player makes a move, the pieces must flip to keep the perspective right
    def flipBoard(self):
        '''
        tempBoard = []
        for row in range(len(self.board)):
        tempRow = []
        for col in range(len(self.board[0])):
        tempRow.append(None)
        tempBoard.append(tempRow)

        for row in range(len(self.board)):
        for col in range(len(self.board[0])):
            tempBoard[row][col] = self.board[len(self.board) - 1 - row][col]
        self.board = tempBoard
        '''
        self.outlineRow = chess.boardSize - 1 - self.outlineRow
        self.outlineCol = chess.boardSize - 1 - self.outlineCol


    def keyPressed(self, event):
        if (event.key == 'r') and self.gameOver:
            self.appStarted()

        if (event.key== 's'):
            from tkinter.filedialog import asksaveasfile
            files = [('All Files', '*.*'),
                     ('Python Files', '*.py'),
                     ('Text Document', '*.txt')]
            file = asksaveasfile(filetypes = files, defaultextension = files)


    def mousePressed(self, event):
        row,col = self.getCell(event.x, event.y)
        self.outlineRow = row
        self.outlineCol = col
        if self.selectedPiece:
            if (self.whiteTurn and self.selectedPiece.color == 'White') or \
               (not self.whiteTurn and self.selectedPiece.color == 'Black'):
                if self.chessGame.movePiece(self.selectedPiece, row, col):
                    self.flipBoard()
                    self.chessGame.flipPieces()
                    self.whiteTurn = not self.whiteTurn
                    self.moves.append((row,col,self.selectedPiece.color))
                    return

        self.selectedPiece = self.chessGame.getPieceAtPosition(row, col)


    #similar to getCell from lecture, just without margins
    def getCell(self, x, y):
        return int(y/self.cellSize), int(x/self.cellSize)

    def drawMoves(self,canvas):
        for i in range(len(self.moves)):
            if self.moves[i][2] == 'White':
                player = 'White'
                row = 8 - self.moves[i][0]
                col = chr(ord('a') + self.moves[i][1])
            else:
                player = 'Black'
                col = chr(ord('h') - self.moves[i][1])
                row = self.moves[i][0] + 1
            canvas.create_text(self.height + (self.width - self.height) // 2,
                           20 + self.cellSize * i,
                           text = f'{player} to {col}{row}')

    def drawBoard(self,canvas):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                x0,y0,x1,y1 = self.getCellBounds(row,col)
                if self.board[row][col]:
                    color = 'grey'
                else:
                    color = 'green'
                if (self.outlineRow or self.outlineCol != None) and \
                   (row,col) == (self.outlineRow, self.outlineCol):
                    canvas.create_rectangle(x0,y0,x1-1,y1-1,
                                            fill=color, outline='yellow')
                else:
                    canvas.create_rectangle(x0,y0,x1,y1,
                                            fill=color,
                                            outline='black')

    def redrawAll(self, canvas):
        self.drawBoard(canvas)
        self.drawPieces(canvas)
        self.drawCoords(canvas)
        self.drawMoves(canvas)

    def getCellBounds(self,row,col):
        x0 = col * self.cellSize
        y0 = row * self.cellSize
        x1 = x0 + self.cellSize
        y1 = y0 + self.cellSize
        return (x0, y0, x1, y1)

def main():
    MyApp(width=1024, height=768)


if __name__ == '__main__':
    main()
