# Sudoku Solver and Visualizer

This project provides a Sudoku solver and visualizer using Python and Pygame. It includes functionality to solve Sudoku puzzles and visualize the solving process.

## Features

- Solve Sudoku puzzles of varying difficulty.
- Visualize the solving process using Pygame.
- Run the solver in headless mode.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/StenerNordnes/Sudoku.git
   cd sudoku-solver
   ```

2. Create a virtual environment (optional but recommended):

   ```sh
   python -m venv .venv

   # Activate the virtual environment (Linux/macOS)
   source venv/bin/activate

   # Activate the virtual environment (Windows)
   .venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Running the Visualizer

To run the Sudoku solver with visualization, execute the following command:

```sh
python Sudoku_solver.py
```

## Example

Here is an example of the visualizer in action:

<img src="./assets/solve_process.gif" alt="Sudoku Visualizer" width="300" height="300">

## Solving Process Using the CSP Class

The `CSP` (_Constraint Satisfaction Problem_) class is used to solve the Sudoku puzzle using a backtracking algorithm. Here is an overview of the solving process:

1. The `backtracking_search` method is called with the initial Sudoku board.
2. The current assignment is checked for consistency using the `isConsistent` method.
3. If the current assignment is not consistent, the algorithm backtracks by returning `None`.
4. An unassigned variable (i.e. an empty cell) is selected using the `select_unassigned` method.
5. If all variables are assigned, the puzzle is solved and the solution is returned.
6. The possible values for the selected variable are fetched from `self.domains[var]` and is shuffled to for an opportunity to solve the puzzle faster.
7. For each value in the domain, the value is assigned to the variable and the `backtrack` method is called recursively.
8. If the recursive call returns a valid solution, the solution is returned.
9. If the recursive call returns `None`, the value is removed from the assignment and the next value is tried.
10. If no value in the domain results in a valid solution, the algorithm backtracks by returning `None`.
