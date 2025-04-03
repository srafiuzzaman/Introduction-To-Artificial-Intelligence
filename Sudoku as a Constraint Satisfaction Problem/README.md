# Homework Assignment 2: Sudoku as a Constraint Satisfaction Problem
CS 580: Introduction to Artificial Intelligence  
Author: Sahad Rafiuzzaman  
Date: 03/02/2025

## Overview
This project is a graphical Sudoku Solver using Constraint Satisfaction Problems (CSP) built using Python (Tkinter).  
The solver uses Backtracking Search with two variations:
1. Simple Backtracking - A standard recursive backtracking approach.
2. Smart Backtracking  - An optimized version using heuristics:
   - Minimum Remaining Values (MRV) - Choose the cell with the fewest values.  
   - Least Constraining Value (LCV) - Try values that minimize future problems.  
   - Forward Checking (FC) - Eliminate invalid values from neighboring cells when assigning a value. 

A Graphical User Interface (GUI) lets users:  
- Pick a puzzle (Easy, Medium, Hard, or Evil).  
- See the Sudoku grid.  
- Solve it using Simple or Smart Backtracking.  
- Get results on runtime, correct assignments, incorrect assignments, and total assignments.  

The Sudoku Solver is based on the original csp.py code AIMA (Artificial Intelligence: A Modern Approach) Python library.

## Features
- Graphical User Interface (GUI) using Tkinter.
- Two backtracking solvers (Simple & Smart)
- Constraint propagation for efficiency
- Performance analysis (runtime and assignments)
- Predefined test puzzles (Easy, Medium, Hard, or Evil)  

## Installation
Be sure to have Python installed along with the following libraries:
* tkinter - GUI framework for Python
* time - Measure runtime
* messagebox (from tkinter) - Display pop-up messages
* deepcopy (from copy) - Creates a copy of nested lists. Used for the Sudoku puzzles.

### Install Dependencies
The following packages must be installed manually: sortedcontainers
- To install the sortedcontainers package, run the following:  
```pip install sortedcontainers```

## How to Run
Once the dependencies are installed, run the following command to start the Sudoku Solver GUI:
```python Sudoku.py```
 
## Operating Sudoku.py
This will launch the Tkinter window, where you can:
- Select a puzzle difficulty (Easy, Medium, Hard, or Evil)
- Solve the puzzle using either:
  - Simple Backtracking
  - Smart Backtracking (MRC = LCV + Forward Checking)
  - Or click the back button to select a different puzzle difficulty. 
- View performance metrics in the pop-up messagebox (runtime, correct assignments, incorrect assignments, and total assignments)

## How it Works
1. Formulating Sudoku as a CSP 
   - Variables: Each empty cell in the 9x9 Sudoku grid. 
   - Domains: Possible values (1-9) for each variable. 
   - Constraints: Ensure that no two identical numbers appear in the same row, column, or 3x3 sub-grid

2. Simple Backtracking Algorithm
   1. Picks an unassigned cell.
   2. Tries values 1-9.
   3. Checks if the value violates any constraints.
   4. If no values work, it backtracks.

3. Smart Backtracking Algorithm  
   - Optimize backtracking using:
     - Minimum Remaining Values (MRV): Choose the cell with the fewest values.
     - Least Constraining Value (LCV): Try values that minimize future problems.
     - Forward Checking: Eliminate invalid values from neighboring cells when assigning a value.
     
4. Performance Analysis  
   - For each Sudoku puzzle, the program records:
     - Runtime in milliseconds
     - Correct Assignments: The number of successful assignments made.
     - Incorrect Assignments: The number of failed assignments made.
     - Total Assignments: Total number of assignments attempted (both correct and incorrect).

## File Structure
1. Main.py
   - Main GUI program 
2. Sudoku_CSP.py
   - Modified csp.py code from AIMA Library
3. search.py
   - Search algorithm file from AIMA Library
4. utils.py
   - Utility functions file from AIMA Library
5. README.md
   - Documentation (this file)
6. Sudoku as a CSP Instructions.pdf
   - Assignment Instructions
7. Sudoku as a CSP Analysis Report.pdf
   - Analysis Report
8. Screenshots of Solutions and results
   1. Easy Sudoku Simple Screenshot.jpg
   2. Easy Sudoku Smart Screenshot.jpg
   3. Medium Sudoku Simple Screenshot.jpg
   4. Medium Sudoku Smart Screenshot.jpg
   5. Hard Sudoku Simple Screenshot.jpg
   6. Hard Sudoku Smart Screenshot.jpg
   7. Evil Sudoku Simple Screenshot.jpg
   8. Evil Sudoku Smart Screenshot.jpg

## Performance Metrics
The table below compare the Simple Backtracking and Smart Backtracking solvers based on the four predefined puzzles.  
Each solver is evaluated on Runtime (ms), Correct Assignments, Incorrect assignments, and Total Assignments.

| Puzzle | Solver Type | Runtime (ms) | Correct Assignments | Incorrect Assignments | Total Assignments |
|--------|-------------|--------------|---------------------|-----------------------|-------------------|
| Easy   | Simple      | 3.51         | 89                  | 22                    | 111               |
| Easy   | Smart       | 4.5          | 81                  | 18                    | 99                |
| Medium | Simple      | 8.51         | 88                  | 30                    | 118               |
| Medium | Smart       | 4.51         | 82                  | 31                    | 113               |
| Hard   | Simple      | 151.45       | 98                  | 35                    | 133               |
| Hard   | Smart       | 14.51        | 84                  | 48                    | 132               |
| Evil   | Simple      | 267.01       | 89                  | 35                    | 124               |
| Evil   | Smart       | 6.51         | 83                  | 48                    | 131               |

### Column Descriptions
- Puzzle: The difficulty level of the Sudoku puzzle (Easy, Medium, Hard, or Evil).
- Solver Type: 
  - Simple: Simple backtracking.  
  - Smart: Smart backtracking using MRV, LCV, and Forward Checking.
- Runtime (ms): Time taken to solve the puzzle in milliseconds.
- Correct Assignments: The number of successful assignments made.
- Incorrect Assignments: The number of failed assignments made.
- Total Assignments: Total number of assignments attempted (both correct and incorrect).

### Key Observations
- Smart Backtracking is generally faster than Simple Backtracking, especially for harder puzzles.  
- For Easy puzzles, the Smart solver has slightly higher runtime due to the added heuristic overhead.  
- For Hard and Evil puzzles, Smart Backtracking significantly reduces runtime while keeping assignments comparable.  
- Incorrect assignments are higher in Smart Backtracking in medium, hard, and evil level puzzles.

### Conclusion
- Smart Backtracking performs better on more complex puzzles, reducing overall solving time.
- Simple Backtracking can be effective for smaller grids, but becomes inefficient for difficult puzzles.

## Acknowledgments
This project was developed with the help of various resources:
- AIMA Python GitHub Library: https://github.com/aimacode
- AIMA Textbook: Artificial Intelligence: A Modern Approach: https://aima.cs.berkeley.edu/
- Tkinter Learning Resource: https://www.youtube.com/@Codemycom
- Markdown Formatting Guide: https://www.jetbrains.com/help/pycharm/markdown.html

## Future Improvements
1. Add a Random mode which would generate a new random Sudoku puzzle and solve it using the existing Simple and Smart backtracking solvers. Something similar to the Homework Assignment 1: The 15-Puzzle Problem Solver.
2. Add a real-time solving animation in the GUI to visually show how numbers are placed step by step.
3. Allow users to input values and solve them using the existing Simple and Smart backtracking solvers.
