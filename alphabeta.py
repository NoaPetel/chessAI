import eval
import chess

MAX_DEPTH = 4

class AlphaBeta:
    def __init__(self, side, depth=MAX_DEPTH):
        self.side = side
        self.depth = depth
        
    def run(self, board, depth=None, alpha=float('-inf'), beta=float('inf')):
        if depth is None:
            depth = self.depth
            
        if board.is_game_over() or depth == 0:
            v = eval.run(board)
            return v, None
            
        best_move = None
        if board.turn != self.side:  # Minimizing player
            v = float('inf')
            for move in board.legal_moves:
                board.push_uci(move.uci())
                score, _ = self.run(board, depth - 1, alpha, beta)
                board.pop()
                
                if score < v:
                    v = score
                    best_move = move
                    
                if v <= alpha:  # Pruning condition for minimizing player
                    return v, best_move
                    
                beta = min(beta, v)
        else:  # Maximizing player
            v = float('-inf')
            for move in board.legal_moves:
                board.push_uci(move.uci())
                score, _ = self.run(board, depth - 1, alpha, beta)
                board.pop()
                
                if score > v:
                    v = score
                    best_move = move
                    
                if v >= beta:  # Pruning condition for maximizing player
                    return v, best_move
                    
                alpha = max(alpha, v)
                
        return v, best_move
