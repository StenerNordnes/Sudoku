from Sudoku_solver import main, SudokuDifficulty
import os
import random


def removeSlots(board, difficulty: SudokuDifficulty = SudokuDifficulty.hard):
    if difficulty == SudokuDifficulty.easy:
        slots = 20
    elif difficulty == SudokuDifficulty.medium:
        slots = 30
    elif difficulty == SudokuDifficulty.hard:
        slots = 60
    else:
        slots = 70

    indicies = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(indicies)
    indicies = indicies[:slots]

    for i, j in indicies:
        board[i][j] = 0

    return board


def generateBoards(numBoards=10, difficulty: SudokuDifficulty = SudokuDifficulty.hard):
    for i in range(numBoards):
        board = main(headless=True, difficulty=SudokuDifficulty.empty)
        board = removeSlots(board, difficulty)
        with open(f"./generated_boards/board_{i}.txt", "w") as f:
            for row in board:
                f.write("".join(map(str, row)) + "\n")


def purgeBoards():
    for file in os.listdir("./generated_boards"):
        os.remove(f"./generated_boards/{file}")


def solveAllBoards():
    for file in os.listdir("./generated_boards"):
        board = main(boardPath=f"./generated_boards/{file}")


if __name__ == "__main__":
    generateBoards(20, None)
