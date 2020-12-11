# tp0
# David Shao

from cmu_112_graphics import *
from abc import ABC, abstractmethod
import time
import copy
import sys
import chess
import pickle
import gameAI

from tkinter.filedialog import asksaveasfilename, askopenfilename

class MyApp(App):
    #size without margins
    SIZE = 768
    def appStarted(self):
        self.currentTurn = 'White'
        # self.moves = []
        self.board = []
        self.chessGame = chess.ChessGame()
        self.aiMode = False

        self.ai = gameAI.ChessAI(self.chessGame, color='Black')
        self.canCastle = True
        # When a piece is clicked, an outline will be drawn around the piece
        self.outlineRow = None
        self.outlineCol = None
        self.selectedPiece = None
        self.scaledImages = dict()

        self.pawns = ['Pawn','Pawn','Pawn','Pawn','Pawn','Pawn','Pawn','Pawn']
        self.rows = 8
        self.cols = 8
        self.cellSize = self.SIZE // self.rows
        self.startGrey = True
        self.gameOver = False
        self.gameStarted = False
        self.images = {}
        self.initializeBoard()
        self.initializePieces()
        self.okToShowGameOver = True
        self.drawSplashScreen = True
        self.drawLevelScreen = False
        self.toCallAI = False
        self.aiTime = 0
        self.aiMoves = 0
        self.bottomMargin = self.height - self.SIZE
        self.sideMargin = self.width - self.SIZE

    def inFlippedView(self):
        return not self.aiMode and self.currentTurn != 'White'

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
        # loading images from 15-112 lecture notes
        # https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#loadImageUsingFile
        # Pictures downloaded from https://github.com/sense-chess/artwork
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

        for key,value in self.images.items():
            self.scaledImages[key] = self.scaleImage(value, 2/3)



    def drawCapturedPieces(self,canvas):
        blackCount = 0
        whiteCount = 0
        for piece in self.chessGame.captured:
            if piece.color == 'White':
                canvas.create_image(10 + whiteCount * (2/3) * 80, self.SIZE + self.bottomMargin//5 , image=ImageTk.PhotoImage(self.scaledImages[piece.getShortName()]))
                whiteCount += 1
            if piece.color == 'Black':
                canvas.create_image(10 + blackCount * (2/3) * 80, self.SIZE + self.bottomMargin//2 + 10 , image=ImageTk.PhotoImage(self.scaledImages[piece.getShortName()]))
                blackCount += 1
            


    def drawCoords(self, canvas):
         if self.currentTurn == 'White':
             for row in range(chess.boardSize):
                 canvas.create_text(8,row * self.cellSize + 15,
                                    text = f'{8 - row}', fill = '#99FFCC')
                 canvas.create_text(self.cellSize - 16 + row * self.cellSize,self.SIZE - 20,
                                    text = chr(ord('a') + row), fill = '#99FFCC')
         else:
             for row in range(len(self.board)):
                 canvas.create_text(self.SIZE - 8,
                                    row * self.cellSize + 15,
                                    text = f'{row + 1}', fill = '#99FFCC')
                 canvas.create_text(16 + row * self.cellSize,
                                    self.SIZE - 20,
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
    
    def chooseLevelScreen(self,canvas):
        canvas.create_text(self.height//2, self.height//2, text='Choose the AI Difficulty: Press 1 for easy, 2 for medium, and 3 for hard')

    # every time player makes a move, the pieces must flip to keep the perspective right
    def flipBoard(self):
        
        self.outlineRow = chess.boardSize - 1 - self.outlineRow
        self.outlineCol = chess.boardSize - 1 - self.outlineCol
    
    def rebuild(self,gameInfo):
        self.aiMode = gameInfo['mode']
        self.ai.changeLevel(gameInfo['AI Level'])
        color = self.chessGame.rebuildFromMoves(gameInfo['moves'])
        self.currentTurn = 'Black' if color == 'White' else 'White'


    def keyPressed(self, event):
        '''
        Saving and loading file syntax from https://docs.python.org/3/library/dialog.html
        The logic for loading a game state is through pickle
        I save the game by saving the move history, along with the AI Mode and Level
        We can rebuild the game with the informatin we just saved
        '''
        if (event.key== 's'):
            
            files = [('Chess Game File', '*.game')]
            filename = asksaveasfilename(filetypes = files, defaultextension = files)
            if not filename:
                return
            
            gameInfo = {
                'mode': self.aiMode,
                'AI Level': self.ai.getLevel(),
                'moves' : self.chessGame.moves
            }

            pickle.dump(gameInfo, open(filename, "wb"))

        elif (event.key== 'l'):
            # cannot load in the middle of the game
            if self.gameStarted:
                return

            files = [('Chess Game File', '*.game')]
            filename = askopenfilename(filetypes = files, defaultextension = files)
            if filename:
                gameInfo = pickle.load(open(filename, "rb"))
                print(gameInfo)
                self.rebuild(gameInfo)
                self.gameStarted = True
                self.drawLevelScreen = False
                self.drawSplashScreen = False

        elif event.key == 'R':
            self.appStarted()
        elif event.key == '?' and self.currentTurn == 'White' and self.aiMode:
            move = self.ai.nextMove('White')
            piece,AIrow,AIcol,_ = move
            print(f'{piece} to {AIrow} {AIcol}')
            self.outlineRow = piece.row
            self.outlineCol = piece.col
            col = chr(ord('a') + AIcol)
            self.showMessage(f'AI recomends you move highlighted piece to {col} {8-AIrow}')
            
        elif event.key == 'S' and self.drawSplashScreen:
            self.aiMode = False
            self.drawSplashScreen = False
            self.gameStarted = True
        elif event.key == 'A' and self.drawSplashScreen:
            self.aiMode = True
            self.drawSplashScreen = False
            self.drawLevelScreen = True
        elif event.key == 'u' and not self.aiMode:
            self.undoStep()
        elif event.key == '1' and self.drawLevelScreen:
            self.drawLevelScreen = False
            self.ai.changeLevel(1)
            self.gameStarted = True
        elif event.key == '2' and self.drawLevelScreen:
            self.drawLevelScreen = False
            self.ai.changeLevel(2)
            self.gameStarted = True
        elif event.key == '3' and self.drawLevelScreen:
            self.drawLevelScreen = False
            self.ai.changeLevel(3)
            self.gameStarted = True


    def undoStep(self):
        if self.chessGame.undoLastMove():
            self.currentTurn = 'Black' if self.currentTurn == 'White' else 'White'        

    def mousePressed(self, event):
        if not self.gameStarted or self.chessGame.gameOver:
            return
        row,col = self.getCell(event.x, event.y)
        if row < 0 or row > 7 or col < 0 or col > 7:
            return 
        self.outlineRow = row
        self.outlineCol = col
        if self.inFlippedView():
            row = chess.boardSize - 1 - row
            col = chess.boardSize - 1 - col
        
        if self.selectedPiece:                   
            if self.aiMode:
                if (self.currentTurn=='White' and self.selectedPiece.color == 'White'):
                    if self.chessGame.movePiece(self.selectedPiece, row, col):
                        #self.moves.append((row,col,self.selectedPiece.color))
                        self.currentTurn = 'Black'
                        self.toCallAI = True
                        self.selectedPiece = None
                        return
            elif ((self.currentTurn=='White' and self.selectedPiece.color == 'White') or \
               (self.currentTurn == 'Black' and self.selectedPiece.color == 'Black')):
                if self.chessGame.movePiece(self.selectedPiece, row, col):
                    # self.moves.append((row,col,self.selectedPiece.color))
                    self.currentTurn = 'Black' if self.currentTurn == 'White' else 'White'

                    self.flipBoard()

        self.selectedPiece = self.chessGame.getPieceAtPosition(row, col)

    def timerFired(self):
        if self.chessGame.gameOver and self.okToShowGameOver:
            self.showMessage(self.chessGame.winner + " wins!")
            self.okToShowGameOver = False 
       
        if self.aiMode and self.toCallAI:
            self.toCallAI = False
            self.makeAIMove()
                        
    def makeAIMove(self):
        assert self.currentTurn == 'Black', "ai is black"
        
        start = time.time()
        move = self.ai.nextMove()
        end = time.time()
        self.updateAITime(end - start)
        if move is None:
            print("You win!")
            self.showMessage("Congrats, you win!!")
            return
        piece,AIrow,AIcol,_ = move

        #print("AI move: ", piece, AIrow,AIcol)
        #print("current move# ", len(self.chessGame.moves))

        self.chessGame.movePiece(piece, AIrow, AIcol)
        self.currentTurn = 'White'
        self.outlineRow = AIrow
        self.outlineCol = AIcol
        # check for end game
        self.chessGame.checkForStatus('White')
        #    self.showMessage("AI wins!")
        #    self.okToShowGameOver = False 

    
    def updateAITime(self, duration):
        self.aiMoves +=1
        self.aiTime += duration
        print(f"ai move time {duration}, avg={self.aiTime/self.aiMoves}")
    
        
    # similar to getCell from lecture, just without margins
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getCell(self, x, y):
        return int(y/self.cellSize), int(x/self.cellSize)

    def drawMoves(self,canvas):
        steps = len(self.chessGame.moves)
        # only want to print the most recent 40 moves
        if len(self.chessGame.moves) > 40:
            startIndex = steps - 1 - 40
        else:
            startIndex = 0
        for i in range(startIndex, steps):
            piece,_,_,row, col,_ = self.chessGame.moves[i]
            colStr = chr(ord('a') + col)
            canvas.create_text(self.SIZE + self.sideMargin // 2,
                           20 + i * 20,
                           text = f'{piece.color[0]} to {colStr}{8 - row }')
          


    def drawBoard(self,canvas):
        canvas.create_rectangle(0,0,self.width,self.height, fill='#D3D3D3')
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
                if self.selectedPiece:
                    
                    if self.selectedPiece.color == self.currentTurn:
                        for move in self.selectedPiece.getLegalMoves(self.chessGame):
                            self.createHintCell(canvas, move)

    def createHintCell(self, canvas, position):
        _, row, col, _ = position
        if self.currentTurn == 'Black':
            row = 7-row
            col = 7-col
        x0,y0,x1,y1 = self.getCellBounds(row, col)

        canvas.create_rectangle(x0,y0,x1-1,y1-1,
                                fill='orange')

    def drawInitialScreen(self,canvas):
        canvas.create_text(self.width//2, self.height//2, text = "Press 'A' for AI Mode")
        canvas.create_text(self.width//2, self.height//2 + 15, text = "Press 'S' for Single Player Mode With Flipped Board")
        canvas.create_text(self.width//2, self.height//2 + 30, text = "Press 's' to save an unfinished game")
        canvas.create_text(self.width//2, self.height//2 + 45, text = "Press 'l' to load a saved game")
        canvas.create_text(self.width//2, self.height//2 + 60, text = "Press 'R' to restart at any time")
    
    def redrawAll(self, canvas):
        if self.drawSplashScreen:
            self.drawInitialScreen(canvas)
            return 
        if self.drawLevelScreen:
            self.chooseLevelScreen(canvas)
            return 
        self.drawBoard(canvas)
        self.drawPieces(canvas)
        self.drawCoords(canvas)
        self.drawMoves(canvas)
        self.drawCapturedPieces(canvas)
       
    # from 112 lecture
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    def getCellBounds(self,row,col):
        x0 = col * self.cellSize
        y0 = row * self.cellSize
        x1 = x0 + self.cellSize
        y1 = y0 + self.cellSize
        return (x0, y0, x1, y1)

def main():
    MyApp(width=900, height=900)


if __name__ == '__main__':
    main()
