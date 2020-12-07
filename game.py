# tp0
# David Shao

from cmu_112_graphics import *
from abc import ABC, abstractmethod
import time
import copy
import sys
import chess
import gameAI

class MyApp(App):
    def appStarted(self):
        self.whiteTurn = True
        self.moves = []
        self.board = []
        self.chessGame = chess.ChessGame()
        self.aiMode = False

        self.ai = gameAI.ChessAI(self.chessGame, color='Black')
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
        self.okToShowGameOver = True
        self.drawSplashScreen = True
        self.toCallAI = False
        self.aiTime = 0
        self.aiMoves = 0

    def inFlippedView(self):
        return not self.aiMode and not self.whiteTurn

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
            row, col = piece.row, piece.col
            if self.inFlippedView():
                row = chess.boardSize - 1 - row
                col = chess.boardSize - 1 - col

            x0,y0,x1,y1 = self.getCellBounds(row,col)
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
        # have 600 millisecon delay of flipping board
        self.outlineRow = chess.boardSize - 1 - self.outlineRow
        self.outlineCol = chess.boardSize - 1 - self.outlineCol


    def keyPressed(self, event):
        if (event.key == 'R'):
            self.appStarted()
        '''
        if (event.key== 's'):
            from tkinter.filedialog import asksaveasfile
            files = [('All Files', '*.*'),
                     ('Python Files', '*.py'),
                     ('Text Document', '*.txt')]
            file = asksaveasfile(filetypes = files, defaultextension = files)
        '''
        if event.key == 'S' and self.drawSplashScreen:
            self.aiMode = False
            self.drawSplashScreen = False
        if event.key == 'A' and self.drawSplashScreen:
            self.aiMode = True
            self.drawSplashScreen = False

    def mousePressed(self, event):
        row,col = self.getCell(event.x, event.y)
        self.outlineRow = row
        self.outlineCol = col
        if self.inFlippedView():
            row = chess.boardSize - 1 - row
            col = chess.boardSize - 1 - col
        
        if self.selectedPiece:                   
            if self.aiMode:
                if (self.whiteTurn and self.selectedPiece.color == 'White'):
                    if self.chessGame.movePiece(self.selectedPiece, row, col):
                        self.moves.append((row,col,self.selectedPiece.color))
                        self.whiteTurn = not self.whiteTurn
                        self.toCallAI = True
            elif ((self.whiteTurn and self.selectedPiece.color == 'White') or \
               (not self.whiteTurn and self.selectedPiece.color == 'Black')):
                if self.chessGame.movePiece(self.selectedPiece, row, col):
                    self.moves.append((row,col,self.selectedPiece.color))
                    self.whiteTurn = not self.whiteTurn

                    self.flipBoard()

        self.selectedPiece = self.chessGame.getPieceAtPosition(row, col)

    def timerFired(self):
        if self.chessGame.gameOver and self.okToShowGameOver:
            self.showMessage(self.chessGame.winner + " wins!")
            self.okToShowGameOver = False 
        #if self.toFlip > 0:
        #    self.toFlip -= 1
        #    if self.toFlip == 0:

        if self.aiMode and self.toCallAI:
            self.toCallAI = False
            self.makeAIMove()
            
            
    def makeAIMove(self):
        assert not self.whiteTurn, "ai is black"
        
        start = time.time()
        move = self.ai.nextMove()
        end = time.time()
        self.updateAITime(end - start)
        if move is None:
            print("You win!")
            self.showMessage("Congrats, you win!!")
            return
        piece,AIrow,AIcol = move

        #print("AI move: ", piece, AIrow,AIcol)
        #print("current move# ", len(self.chessGame.moves))

        self.chessGame.movePiece(piece, AIrow, AIcol)

        self.outlineRow = AIrow
        self.outlineCol = AIcol
        self.whiteTurn = not self.whiteTurn

    def updateAITime(self, duration):
        self.aiMoves +=1
        self.aiTime += duration
        print(f"ai move time {duration}, avg={self.aiTime/self.aiMoves}")


        
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

    def drawInitialScreen(self,canvas):
        canvas.create_text(self.width//2, self.height//2, text = 'Press A for AI Mode')
        canvas.create_text(self.width//2, self.height//2 + 15, text = 'Press S for Single Player Mode With Flipped Board')

    def redrawAll(self, canvas):
        if self.drawSplashScreen:
            self.drawInitialScreen(canvas)
            return 
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
