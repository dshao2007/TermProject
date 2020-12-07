
import random

from evaluator import ChessEval

class ChessAI(object):

    INF = 8000

    def __init__(self,game,color):
        self.game = game
        self.evaluator = ChessEval(game)
        self.color = color
        self.drunkMode = False
        self.points = {'Pawn': 10, 'Knight': 30, 'Bishop': 30, 'Rook': 50, 'Queen': 90, 'King': 200} 

    def nextMove(self):
        results = self.game.getAllLegalMoves(self.color)
        if len(results) == 0:
            return None
        
        if self.drunkMode:
           # return a random move
           index = random.randint(0,len(results) - 1)
           return results[index]
        
        move, _ = self.minimax(-self.INF, self.INF, self.color)
        return move    
    

    # Minimax is a completely new concept to me, and I the reference from
    # https://www.chessprogramming.org/Search to learn about it
    # All of the code is mine, with the exception of alpha beta pruning, which is
    # a standard template I got from the website. I am still getting it to work
    def minimax(self, alpha, beta, color, depth=3):
        results = self.game.getAllLegalMoves(color)
        score = self.getScore()
        if depth == 0:
            #print("ai move: depth 0")
            #print(self.game.printMoves())
            return None, score
        
        '''if self.game.inCheck('White') and self.game.checkMate('White'):
            return score
        if self.game.inCheck('Black') and self.game.checkMate('Black'):
            return score
        '''

        if len(results) == 0:
            # print("ai move: no legal moves")
            return None, score
        
        if color == 'White':
            otherColor = 'Black'
        else:
            otherColor = 'White'
        if self.color == color:        
            move = None
            maxVal = -self.INF
            # print(f'{depth} max the move for {color}')
            for i in range(len(results)):
                self.game.movePiece(results[i][0], results[i][1], results[i][2],
                                    aiMode=True, simulate=False)
                
                _, eval = self.minimax(alpha, beta, otherColor, depth - 1)
                # maxVal = max(eval, maxVal)
                if eval > maxVal:
                    move = results[i]
                    maxVal = eval
                self.game.undoLastMove()
                alpha = max(alpha, maxVal)
                '''if beta <= alpha:
                    break'''
            # moves.append(move)
            return (move, maxVal)
        else:
            minVal = self.INF
            # print(f'{depth} min the move for {color}')
            move = None
            for i in range(len(results)):
                self.game.movePiece(results[i][0], results[i][1], results[i][2],
                                    aiMode=True, simulate=False)
                
                _, eval = self.minimax(alpha, beta, otherColor, depth - 1)
                self.game.undoLastMove()
                # minVal = min(eval, minVal)
                if eval < minVal:
                    minVal = eval
                    move = results[i]
                beta = min(beta, minVal)
                
                '''if beta <= alpha:
                    break'''
            return move, minVal

    def getScore(self):
        blackScore, whiteScore = self.evaluator.getScore()

        if self.game.inCheck('Black') and self.game.checkMate('Black'):
            blackScore -= 900
        if self.game.inCheck('White') and self.game.checkMate('White'):
            whiteScore -= 900

        if self.color == 'White':
            return whiteScore - blackScore
        else:
            return blackScore - whiteScore

    def getScoreSimple(self):
        w = self.getWhiteScore()
        b = self.getBlackScore()
        if self.color == 'White':
            return w - b
        else:
            return b - w
    
    def getWhiteScore(self):
        score = 0
        for piece in self.game.getPieces():
            if piece.color == 'White':
                score += self.points[piece.name]
        if self.game.inCheck('Black') and self.game.checkMate('Black'):
            score += 900
        
        return score

    def getBlackScore(self):
        score = 0
        for piece in self.game.getPieces():
            if piece.color == 'Black':
                score += self.points[piece.name]
        if self.game.inCheck('White') and self.game.checkMate('White'):
            score += 900
        
        return score

