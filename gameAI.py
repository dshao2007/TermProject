
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
        self.depth = 3
    
    def changeLevel(self,level):
        self.depth = level + 1

    def getLevel(self):
        return self.depth - 1
    
    def nextMove(self, playerColor=None):
        if playerColor is None:
            playerColor = self.color
        results = self.game.getAllLegalMoves(playerColor, fullValidate=False)
        if len(results) == 0:
            return None
        move, _ = self.minimax(-self.INF, self.INF, playerColor, playerColor, self.depth)
        return move    
    

    # Minimax is a completely new concept to me, and I the reference from
    # https://www.chessprogramming.org/Search to learn about it
    # All of the code is mine, with the exception of alpha beta pruning, which is
    # a standard template I got from the website. 
    def minimax(self, alpha, beta, color, playerColor, depth):
        results = self.game.getAllLegalMoves(color, fullValidate=False)
        score = self.getScore()
        if playerColor == 'White':
            score = -score
        
        if depth == 0:
            return None, score
        
        if len(results) == 0:
            return None, score
        
        if color == 'White':
            otherColor = 'Black'
        else:
            otherColor = 'White'
        if playerColor == color:
            move = None
            maxVal = -self.INF
            for i in range(len(results)):
                if self.game.movePiece(results[i][0], results[i][1], results[i][2],
                                       aiMode=True, simulate=False):
                
                    _, eval = self.minimax(alpha, beta, otherColor, playerColor, depth - 1)
                    # maxVal = max(eval, maxVal)
                    if eval > maxVal:
                        move = results[i]
                        maxVal = eval
                    self.game.undoLastMove()
                    alpha = max(alpha, maxVal)
                    if beta <= alpha:
                        break
                else:
                    pass
            # moves.append(move)
            return (move, maxVal)
        else:
            minVal = self.INF
            move = None
            for i in range(len(results)):
                if not self.game.movePiece(results[i][0], results[i][1], results[i][2],
                                           aiMode=True, simulate=False):
                    continue
                
                _, eval = self.minimax(alpha, beta, otherColor, playerColor, depth - 1)
                self.game.undoLastMove()
                # minVal = min(eval, minVal)
                if eval < minVal:
                    minVal = eval
                    move = results[i]
                beta = min(beta, minVal)
                
                if beta <= alpha:
                    break
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
    
    # Assign large score to checkmate so AI goes for the win
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

