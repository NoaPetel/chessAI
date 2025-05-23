import chess
from stockfish import Stockfish
import csv
from nn_eval import NNEval
from chess_eval_dataset import ChessEvalDataset
from torch.utils.data import DataLoader
import torch
import torch.nn as nn
import ast

stockfish = Stockfish(
    path="./stockfish/stockfish-windows-x86-64-avx2.exe",
)
stockfish.set_elo_rating(3000)


def generate_date(stockfish):
    rows = []

    for i in range(10):
        print(f"game {i}")
        print(len(rows))
        board = chess.Board()

        while (not board.is_game_over()):
            # Make the move
            fen = board.fen()
            stockfish.set_fen_position(fen)
            evaluation = stockfish.get_evaluation()
            move = stockfish.get_best_move(250)

            # Save Data
            rows.append([fen, evaluation])
            board.push_uci(move)

    with open("stockfish_dataset.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["FEN", "Evaluation"])
        writer.writerows(rows)


def train_NN():
    NN = NNEval()

    fen_eval_list = []

    with open("stockfish_dataset.csv", "r", newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header if there is one
        for row in reader:
            fen, eval_str = row
            try:
                eval_dict = ast.literal_eval(eval_str)
                if eval_dict["type"] == "cp":
                    eval_score = eval_dict["value"]
                elif eval_dict["type"] == "mate":
                    eval_score = 10000 * (-1 if eval_dict["value"] < 0 else 1)
                else:
                    continue
                fen_eval_list.append((fen, eval_score))
            except:
                continue  # Skip bad rows

    dataset = ChessEvalDataset(fen_eval_list)
    train_loader = DataLoader(dataset, batch_size=64, shuffle=True)
    NN.train(train_loader)
    NN.save("nn_eval.pth")


def evaluate_NN():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load model
    model = NNEval().to(device)
    model.load()

    # Load dataset
    fen_eval_list = []
    with open("stockfish_dataset.csv", "r") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header if present
        for row in reader:
            fen, eval_str = row
            try:
                eval_dict = ast.literal_eval(eval_str)
                if eval_dict["type"] == "cp":
                    eval_score = eval_dict["value"]
                elif eval_dict["type"] == "mate":
                    eval_score = 10000 * (-1 if eval_dict["value"] < 0 else 1)
                else:
                    continue
                fen_eval_list.append((fen, eval_score))
            except:
                continue

    dataset = ChessEvalDataset(fen_eval_list)
    # Evaluation
    for x, y in dataset:
        pred = model.forward(x)
        print(pred, y)

evaluate_NN()