
# Sudoku/Minesweeper Solver Program

![Sudoku Solver](https://github.com/tarun2001sharma/Sudoku-Minesweeper-Solver/assets/59308544/91f23b12-07bb-4c23-8b7b-991055f56d29) ![Minesweeper Solver](https://github.com/tarun2001sharma/Sudoku-Minesweeper-Solver/assets/59308544/d3edf38a-693c-4dd7-af74-32ccf26a5b89)  
*Figure: Left - Sudoku Solver Interface, Right - Minesweeper Solver Interface*

This project presents a versatile solver for both Sudoku and Minesweeper puzzles, leveraging the Davis-Putnam-Logemann-Loveland (DPLL) algorithm. The solver converts puzzles into Conjunctive Normal Form (CNF) and employs propositional logic to find solutions efficiently. This README provides all the necessary information to get started, including system requirements, installation instructions, and how to use the solver.

## Project Structure

- `main.py`: The entry point of the program. It parses command-line arguments and coordinates the solving process.
- `helper.py`: Contains utility functions for parsing puzzles, generating CNF clauses, and converting solutions back into a readable format.
- `DPLL.py`: Implements the DPLL algorithm, handling logical deductions, recursive backtracking, and solution finding.

## Prerequisites

Ensure Python 3.x is installed on your system. You can verify your Python version with the following command:

```bash
python --version
```

This project has been tested with Python 3.11.4. Adjustments may be necessary for compatibility with other versions.

## Installation

No additional installation steps are required beyond having Python 3.x installed. Simply clone or download this repository to your local machine.

## Usage

To solve a puzzle, run `main.py` with the puzzle input as command-line arguments. The input format for Sudoku is 'rc=v', where 'r' represents the row, 'c' the column, and 'v' the value.

### Solving Sudoku

```bash
python main.py 12=5 14=3 ...
```

### Solving Minesweeper

Currently, the project focuses on Sudoku puzzles. Support for Minesweeper puzzle inputs is planned for future updates.

### Modes

- **Verbose Mode (-v)**: Provides detailed logs of the solving process. Useful for debugging or understanding the algorithm's steps.

```bash
python main.py -v 12=5 14=3 ...
```

- **Random Mode (-random)**: Instead of the default lexicographical guessing, this mode randomly selects literals for guessing. This can significantly reduce the runtime for complex puzzles.

```bash
python main.py -random 12=5 14=3 ...
```

## Runtime Performance

Runtime varies based on the puzzle's difficulty and the mode selected:

- Lexicographical guessing (Random mode OFF): Ranges from under a second for simple puzzles to approximately 1 hour for extremely difficult ones.
- Random guessing (Random mode ON): Reduces runtime significantly, with even the most challenging puzzles solved within seconds.

## Contributions

This project is open for contributions. Whether you'd like to add new features, improve the algorithm's efficiency, or extend support to Minesweeper puzzles, your input is welcome.

## License

Specify your project's license here, detailing how others can use or contribute to your code.

