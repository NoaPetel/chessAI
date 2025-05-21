import eval 
import chess

def alphabeta(board, alpha, beta):
    if(board.is_game_over()):
        return eval.run(board)
    else:
        if(board.turn == chess.WHITE):
            v = float('inf')
            for move in board.legal_move:
                nextBoard = board.push_san(move)
                v = min(v, alphabeta(nextBoard, alpha, beta))
                if(alpha >= v):
                    return v
                beta = min(beta, v)
        else:
            v = float('-inf')
            for move in board.legal_move:
                
                nextBoard = board.push_san(move)
                v = max(v, alphabeta(nextBoard, alpha, beta))
                if(v >= beta):
                    return v
                alpha = max(alpha, v)
    return v
            
            