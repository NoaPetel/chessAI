import torch
import chess

def fen_to_tensor(fen: str) -> torch.Tensor:
    board = chess.Board(fen)
    tensor = torch.zeros(773)

    # 1. Encode piece planes (12 x 64)
    piece_map = board.piece_map()
    piece_to_index = {
        "P": 0, "N": 1, "B": 2, "R": 3, "Q": 4, "K": 5,
        "p": 6, "n": 7, "b": 8, "r": 9, "q": 10, "k": 11,
    }
    for square, piece in piece_map.items():
        index = piece_to_index[piece.symbol()]
        tensor[index * 64 + square] = 1.0

    offset = 768

    # 2. Side to move (0 = white, 1 = black)
    tensor[offset] = 1.0 if board.turn == chess.BLACK else 0.0
    offset += 1

    # 3. Castling rights
    tensor[offset]     = float(board.has_kingside_castling_rights(chess.WHITE))  # K
    tensor[offset + 1] = float(board.has_queenside_castling_rights(chess.WHITE)) # Q
    tensor[offset + 2] = float(board.has_kingside_castling_rights(chess.BLACK))  # k
    tensor[offset + 3] = float(board.has_queenside_castling_rights(chess.BLACK)) # q
    offset += 4

    # # 4. En passant file (8 bits one-hot)
    # if board.ep_square is not None:
    #     file = chess.square_file(board.ep_square)
    #     tensor[offset + file] = 1.0

    return tensor
