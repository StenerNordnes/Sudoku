import random
import threading
import time
from time import perf_counter

import pygame

from csp import CSP, alldiff

gamesFolder = "games/"


class SudokuDifficulty:
    easy = gamesFolder + "easy.txt"
    medium = gamesFolder + "medium.txt"
    hard = gamesFolder + "hard.txt"
    empty = gamesFolder + "empty.txt"
    very_hard = gamesFolder + "very_hard.txt"


def print_solution(solution, width=9):
    """
    Convert the representation of a Sudoku solution, as returned from
    the method CSP.backtracking_search(), into a Sudoku board.
    """
    for row in range(width):
        for col in range(width):
            print(solution[f"X{row+1}{col+1}"], end=" ")
            if col == 2 or col == 5:
                print("|", end=" ")
        print("")
        if row == 2 or row == 5:
            print("------+-------+------")


class SudokuVisualizer:
    """
    A class that visualizes the Sudoku board using Pygame.
    """

    def __init__(self):
        """
        Initializes the SudokuVisualizer class.
        """
        pygame.init()
        pygame.display.set_caption("Sudoku Solver")
        pygame.font.init()

        self.screenHeight = 500
        self.screenWidth = 500
        self.font = pygame.font.Font(None, 30)
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        self.running = True
        self.lock = threading.Lock()
        self.run_thread = threading.Thread(target=self.run)
        self.run_thread.start()

    def draw_board(self):
        """
        Draws the Sudoku board on the Pygame screen.
        """
        padding = 50
        boxSize = (
            min(self.screenHeight - 2 * padding, self.screenWidth - 2 * padding) // 9
        )
        numberOffset = boxSize // 2 - 10
        totalLength = 9 * boxSize

        self.screen.fill((255, 255, 255))
        for i in range(10):
            if i % 3 == 0:
                thickness = 2
            else:
                thickness = 1
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (padding + i * boxSize, padding),
                (padding + i * boxSize, totalLength + padding),
                thickness,
            )
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (padding, padding + i * boxSize),
                (totalLength + padding, padding + i * boxSize),
                thickness,
            )
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    value = self.font.render(str(self.board[i][j]), True, (0, 0, 0))
                    self.screen.blit(
                        value,
                        (
                            padding + j * boxSize + numberOffset,
                            padding + i * boxSize + numberOffset,
                        ),
                    )

        pygame.display.flip()

    def run(self):
        """
        Runs the Pygame event loop for the Sudoku visualizer.
        """
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.clock = pygame.time.Clock()
        while self.running:
            self.clock.tick(60)
            self.draw_board()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()
        pygame.quit()

    def update_board(self, board: dict[str, str]):
        """
        Updates the Sudoku board with the given values.

        Args:
            board (dict[str, str]): A dictionary representing the Sudoku board.
        """
        with self.lock:
            self.wipe_board()
            for key, value in board.items():
                row, col = int(key[1]) - 1, int(key[2]) - 1
                self.board[row][col] = value

    def wipe_board(self):
        """
        Clears the Sudoku board.
        """
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def end(self):
        """
        Ends the Sudoku visualizer.
        """
        self.running = False

    def get_board(self) -> dict[str, str]:
        """
        Returns the current state of the Sudoku board.

        Returns:
            dict[str, str]: A dictionary representing the Sudoku board.
        """
        return self.board


def update_board_thread(csp: CSP, visualizer):
    """
    Updates the Sudoku board using Constraint Satisfaction Problem (CSP) approach.
    Args:
        visualizer: The visualizer object used to display the Sudoku board.
    Returns:
        None
    Raises:
        None
    """

    # Run the AC-3 algorithm to reduce the domains of the variables
    csp.ac_3()

    start = perf_counter()
    # Use backtracking search to find a solution to the Sudoku problem
    csp.backtracking_search(visualizer=visualizer)

    # Print the time taken to solve the problem
    end = perf_counter()
    print(f"Time: {end - start}")

    # Check if the final assignment is consistent
    print("IS CONSISTENT", csp.isConsistent())

    # Print the solution
    print_solution(csp.assignments)

    # Wait for 5 seconds before ending the visualizer
    time.sleep(5)
    visualizer.end()


def run_headless(csp: CSP, width=9, domains=None, edges=None):
    """
    Updates the Sudoku board using Constraint Satisfaction Problem (CSP) approach.
    Args:
        visualizer: The visualizer object used to display the Sudoku board.
    Returns:
        None
    Raises:
        None
    """

    # Run the AC-3 algorithm to reduce the domains of the variables
    csp.ac_3()

    start = perf_counter()
    # Use backtracking search to find a solution to the Sudoku problem
    csp.backtracking_search()

    # Print the time taken to solve the problem
    end = perf_counter()
    print(f"Time: {end - start}")

    # Print the solution
    print_solution(csp.assignments, width)

    board = [[0 for _ in range(9)] for _ in range(9)]

    for key, value in csp.assignments.items():
        row, col = int(key[1]) - 1, int(key[2]) - 1
        board[row][col] = value

    return board


def main(
    headless=False, difficulty: SudokuDifficulty = SudokuDifficulty.hard, boardPath=None
) -> dict[str, str]:
    boardToSolve = difficulty
    grid = ""
    with open(boardPath or f"./{boardToSolve}") as f:
        grid = f.read().split()

    width = 9
    box_width = 3

    domains = {}
    for row in range(width):
        for col in range(width):
            if grid[row][col] == "0":
                domains[f"X{row+1}{col+1}"] = set(range(1, 10))
            else:
                domains[f"X{row+1}{col+1}"] = {int(grid[row][col])}

    edges = []
    for row in range(width):
        edges += alldiff([f"X{row+1}{col+1}" for col in range(width)])
    for col in range(width):
        edges += alldiff([f"X{row+1}{col+1}" for row in range(width)])
    for box_row in range(box_width):
        for box_col in range(box_width):
            edges += alldiff(
                [
                    f"X{row+1}{col+1}"
                    for row in range(box_row * box_width, (box_row + 1) * box_width)
                    for col in range(box_col * box_width, (box_col + 1) * box_width)
                ]
            )

        # Create a CSP object with the variables, domains, and edges
    csp = CSP(
        variables=[f"X{row+1}{col+1}" for row in range(width) for col in range(width)],
        domains=domains,
        edges=edges,
    )

    if headless:
        return run_headless(csp, width, domains, edges)

    visualizer = SudokuVisualizer()
    update_thread = threading.Thread(
        target=update_board_thread,
        args=(
            csp,
            visualizer,
        ),
    )
    update_thread.start()
    update_thread.join()

    finsihedBoard = visualizer.get_board()
    visualizer.end()
    return finsihedBoard


if __name__ == "__main__":
    main(difficulty=SudokuDifficulty.very_hard)
