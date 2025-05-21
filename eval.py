import chess
from tables import mg_bishop_table, mg_king_table, mg_knight_table, mg_pawn_table, mg_queen_table, mg_rook_table, eg_bishop_table, eg_king_table, eg_knight_table, eg_pawn_table, eg_queen_table, eg_rook_table


WHITE, BLACK = chess.WHITE, chess.BLACK

def piece_index(piece: chess.Piece) -> int:
    return 2 * (piece.piece_type - 1) + (0 if piece.color == chess.WHITE else 1)

mg_value = [82, 337, 365, 477, 1025, 0]
eg_value = [94, 281, 297, 512, 936, 0]

gamephaseInc = [0,0,1,1,1,1,2,2,4,4,0,0]

mg_tables = [None] * 12
eg_tables = [None] * 12

def flip(sq):
    return sq ^ 56

def init_tables():
    global mg_tables, eg_tables

    mg_pesto_table = [mg_pawn_table, mg_knight_table, mg_bishop_table,
                      mg_rook_table, mg_queen_table, mg_king_table]
    eg_pesto_table = [eg_pawn_table, eg_knight_table, eg_bishop_table,
                      eg_rook_table, eg_queen_table, eg_king_table]

    for p in range(6):  # PAWN to KING
        for color in [chess.WHITE, chess.BLACK]:
            idx = 2 * p + color
            mg_tables[idx] = [0] * 64
            eg_tables[idx] = [0] * 64
            for sq in range(64):
                table_sq = sq if color == chess.WHITE else flip(sq)
                mg_tables[idx][sq] = mg_value[p] + mg_pesto_table[p][table_sq]
                eg_tables[idx][sq] = eg_value[p] + eg_pesto_table[p][table_sq]

def run(board):

    mg = [0, 0]
    eg = [0, 0]
    gamePhase = 0
    baseBoard = chess.Board(board.fen())
    for sq in chess.SQUARES:

        piece = baseBoard.piece_at(sq)
        if piece:
            idx = piece_index(piece)
            color = int(piece.color)

            mg[color] += mg_tables[idx][sq]
            eg[color] += eg_tables[idx][sq]
            gamePhase += gamephaseInc[idx]

    side = board.turn
    opp = not side
    mgScore = mg[side] - mg[opp]
    egScore = eg[side] - eg[opp]
    mgPhase = min(gamePhase, 24)
    egPhase = 24 - mgPhase
    return (mgScore * mgPhase + egScore * egPhase) // 24
