



# This is for the minimax algorithm. The 2-D list represents a board, and each number 
# represents a piece's worth relative to other positions on the board
# For example, a player's king on the enemy side is worth negative points, as 
# that can be very risky 
# I got the numbers from https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/
class ChessEval(object):

    PawnWhiteWt = [
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
    ]
    PawnBlackWt = PawnWhiteWt[::-1]
    PawnWhiteLateGame = [
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [8,   10,  10.0,  11.0,  11.0,  12.0,  11.0,  8.0],
        [5,   5,  6.0,  6.0,  6.0,  6.0,  5.0,  5.0],
        [4,   4,  5.0,  5.0,  5.0,  5.0,  4.0,  4.0],
        [3,   3,  4.0,  4.0,  4.0,  4.0,  3.0,  3.0],
        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
    ]
    PawnBlackLateGame = PawnWhiteLateGame[::-1]   
    

    KnightWt = [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
        [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
        [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
        [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
        [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
        [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
    ]

    BishopWhiteWt = [
        [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
        [ -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
        [ -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
        [ -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
        [ -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
        [ -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
        [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
    ]

    BishopBlackWt = BishopWhiteWt[::-1]

    RookWhiteWt = [
    [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [  0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
    ]

    RookBlackWt = RookWhiteWt[::-1]

    QueenWt = [
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
]

    KingWhiteWt = [
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
    [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]
]

    KingBlackWt = KingWhiteWt[::1]

    def __init__(self, game):
        self.game = game
        
    
    def getScore(self):
        whiteScore = 0
        blackScore = 0

        lateGameForWhite = False
        lateGameForBlack = False
        whiteOther = 0
        blackOther = 0
        whiteKP = 0
        blackKP = 0
        
        for piece in self.game.getPieces():
            if piece.color == 'White':
                if piece.name in ['King', 'Pawn']:
                    whiteKP += 1
                else:
                    whiteOther +=1
            if piece.color == 'Black':
                if piece.name in ['King', 'Pawn']:
                    blackKP += 1
                else:
                    blackOther +=1
        if whiteOther < 3:
            lateGameForWhite = True
        if blackOther < 3:
            lateGameForBlack = True

        for piece in self.game.getPieces():
            if piece.name == 'Pawn':
                if piece.color == 'White':
                    if lateGameForWhite:
                        whiteScore += 10 + self.PawnWhiteLateGame[piece.row][piece.col]
                    else:
                        whiteScore += 10 + self.PawnWhiteWt[piece.row][piece.col]
                else:
                    if lateGameForBlack:
                        blackScore += 10 + self.PawnBlackLateGame[piece.row][piece.col]
                    else:
                        blackScore += 10 + self.PawnBlackWt[piece.row][piece.col]
            elif piece.name == 'Rook':
                if piece.color == 'White':
                    whiteScore += 50 + self.RookWhiteWt[piece.row][piece.col]
                else:
                    blackScore += 50 + self.RookBlackWt[piece.row][piece.col]
            elif piece.name == 'Knight':
                if piece.color == 'White':
                    whiteScore += 30 + self.KnightWt[piece.row][piece.col]
                else:
                    blackScore += 30 + self.KnightWt[piece.row][piece.col]
            elif piece.name == 'Bishop':
                if piece.color == 'White':
                    whiteScore += 30 + self.BishopWhiteWt[piece.row][piece.col]
                else:
                    blackScore += 30 + self.BishopBlackWt[piece.row][piece.col]
            elif piece.name == 'Queen':
                if piece.color == 'White':
                    whiteScore += 90 + self.QueenWt[piece.row][piece.col]
                else:
                    blackScore += 90 + self.QueenWt[piece.row][piece.col]
            elif piece.name == 'King':
                if piece.color == 'White':
                    whiteScore += 900 + self.KingWhiteWt[piece.row][piece.col]
                else:
                    blackScore += 900 + self.KingBlackWt[piece.row][piece.col]
        return (blackScore, whiteScore)       
