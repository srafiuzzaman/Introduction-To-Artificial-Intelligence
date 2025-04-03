"""
Sahad Rafiuzzaman
Date: 03/02/2025
CS 580: Introduction to Artificial Intelligence

Homework Assignment 2: Sudoku as a Constraint Satisfaction Problem
This implementation includes:
- A GUI to select and solve Sudoku puzzles.
- Simple and Smart Backtracking algorithms.

Task 1: Formulating Sudoku as a CSP
Variables: Each empty cell in the 9x9 Sudoku grid.
Domains: Possible values (1-9) for each variable.
Constraints: Ensure that no two identical numbers appear in the same row, column, or 3x3 sub-grid

Task 2: Implementing Basic Backtracking Algorithm
Implement a basic backtracking algorithm that:
1. Picks an unassigned cell.
2. Tries values 1-9.
3. Checks if the value violates any constraints.
4. If no values work, it backtracks.

Task 3: Implementing Smart Backtracking Algorithm
Optimize backtracking using:
Minimum Remaining Values (MRV): Choose the cell with the fewest values.
Least Constraining Value (LCV): Try values that minimize future problems.
Forward Checking: Eliminate invalid values from neighboring cells when assigning a value.

Task 4: Performance Analysis
1. Compare runtimes of both algorithms.
2. Count the number of value assignments.
3. Include screenshots of the solutions.
"""

# Importing necessary libraries
import tkinter as tk            # Provides the GUI framework.
import time                     # Used for tracking how long the solver takes.
from tkinter import messagebox  # A Tkinter module that displays pop-up messages.
from copy import deepcopy       # Creates a copy of nested lists. Used for the Sudoku puzzles.

# Importing CSP functions. csp.py is originally from the AIMA GitHub.
from Sudoku_CSP import mrv, lcv, forward_checking, backtracking_search, Sudoku

"""
Predefined starting configurations of Sudoku puzzles
- Each puzzle is stored as a 9x9 lists of lists.
- O represents an empty cell.
"""
sudoku_puzzles = {
    "Easy": [[0, 3, 0, 0, 8, 0, 0, 0, 6],
             [5, 0, 0, 2, 9, 4, 7, 1, 0],
             [0, 0, 0, 3, 0, 0, 5, 0, 0],
             [0, 0, 5, 0, 1, 0, 8, 0, 4],
             [4, 2, 0, 8, 0, 5, 0, 3, 9],
             [1, 0, 8, 0, 3, 0, 6, 0, 0],
             [0, 0, 3, 0, 0, 7, 0, 0, 0],
             [0, 4, 1, 6, 5, 3, 0, 0, 2],
             [2, 0, 0, 0, 4, 0, 0, 6, 0]],

    "Medium": [[3, 0, 8, 2, 9, 6, 0, 0, 0],
               [0, 4, 0, 0, 0, 8, 0, 0, 0],
               [5, 0, 2, 1, 0, 0, 0, 8, 7],
               [0, 1, 3, 0, 0, 0, 0, 0, 0],
               [7, 8, 0, 0, 0, 0, 0, 3, 5],
               [0, 0, 0, 0, 0, 0, 4, 1, 0],
               [1, 2, 0, 0, 0, 7, 8, 0, 3],
               [0, 0, 0, 8, 0, 0, 0, 2, 0],
               [0, 0, 0, 5, 4, 2, 1, 0, 6]],

    "Hard": [[7, 0, 0, 0, 0, 0, 0, 0, 0],
             [6, 0, 0, 4, 1, 0, 2, 5, 0],
             [0, 1, 3, 0, 9, 5, 0, 0, 0],
             [8, 6, 0, 0, 0, 0, 0, 0, 0],
             [3, 0, 1, 0, 0, 0, 4, 0, 5],
             [0, 0, 0, 0, 0, 0, 0, 8, 6],
             [0, 0, 0, 8, 4, 0, 5, 3, 0],
             [0, 4, 2, 0, 3, 6, 0, 0, 7],
             [0, 0, 0, 0, 0, 0, 0, 0, 9]],

    "Evil": [[0, 6, 0, 8, 0, 0, 0, 0, 0],
             [0, 0, 4, 0, 6, 0, 0, 0, 9],
             [1, 0, 0, 0, 4, 3, 0, 6, 0],
             [0, 5, 2, 0, 0, 0, 0, 0, 0],
             [0, 0, 8, 6, 0, 9, 3, 0, 0],
             [0, 0, 0, 0, 0, 0, 5, 7, 0],
             [0, 1, 0, 4, 8, 0, 0, 0, 5],
             [8, 0, 0, 0, 1, 0, 2, 0, 0],
             [0, 0, 0, 0, 0, 5, 0, 4, 0]]
}

class SudokuGUI:
    """SudokuGUI Class - Handles the GUI for Sudoku selection, solving, and visualization."""
    def __init__(self, root):
        self.root = root
        self.root.title("Assignment 2: Sudoku")     # Sets the window title.
        self.root.geometry("750x750")               # Fixed window size
        self.root.resizable(False, False)           # Disable window resizing
        self.root.configure(bg="#74CDED")           # Window background color
        self.difficulty = None                      # Initializes variable - Stores the selected difficulty.
        self.grid = None                            # Initializes variable - Stores the current Sudoku board.
        self.create_welcome_screen()                # Calls to display the main menu.


    def create_welcome_screen(self):
        self.clear_screen()                         # Clears the screen

        # Title Label
        tk.Label(self.root, text="Sudoku as a Constraint Satisfaction Problem", font=("Century", 26),
                 bg="#74CDED").pack(pady=(50, 10))

        # Instruction Label
        tk.Label(self.root, text="Please select a difficulty level", font=("Century", 24),
                 bg="#74CDED").pack(pady=(20,10))

        # Frame to hold the difficulty level buttons
        button_frame = tk.Frame(self.root, bg="#74CDED")
        button_frame.pack(pady=50)

        # Configure grid to make buttons equal size
        for i in range(2):
            button_frame.grid_columnconfigure(i, weight=1)  # Make columns expand equally
            button_frame.grid_rowconfigure(i, weight=1)  # Make rows expand equally

        # Button properties (fixed size)
        button_width = 10
        button_height = 2

        # Buttons in a 2x2 grid
        # When a button is clicked, it calls load_sudoku(difficulty), loading the selected puzzle.
        tk.Button(button_frame, text="E a s y", font=("Arial Rounded MT Bold", 32), fg="#2ECC71",
                  width=button_width, height=button_height, bg="#EAF8E6",
                  command=lambda: self.load_sudoku("Easy")).grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        tk.Button(button_frame, text="M e d i u m", font=("Segoe UI", 32), fg="#3498DB",
                  width=button_width, height=button_height, bg="#D6EAF8",
                  command=lambda: self.load_sudoku("Medium")).grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        tk.Button(button_frame, text="H a r d", font=("Rockwell", 36), fg="#E67E22",
                  width=button_width, height=button_height, bg="#FAE5D3",
                  command=lambda: self.load_sudoku("Hard")).grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        tk.Button(button_frame, text="E v i l", font=("Chiller", 42), fg="#C0392B",
                  width=button_width, height=button_height, bg="#4A0707",
                  command=lambda: self.load_sudoku("Evil")).grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        tk.Label(self.root, text=" Sahad Rafiuzzaman | CS 580 | Assignment 2 ", font=("Century", 18),
                 bg="#74CDED").pack(side="bottom", fill="x", pady=15)


    def load_sudoku(self, difficulty):
        """Load a predefined Sudoku puzzle based on selected difficulty"""
        self.difficulty = difficulty                        # Stores the selected difficulty.
        self.grid = deepcopy(sudoku_puzzles[difficulty])    # Copies the puzzle. Does not modify the original.
        self.create_sudoku_screen()                         # Calls create_sudoku_screen() to show the Sudoku grid.


    def create_sudoku_screen(self):
        """# Display the Sudoku grid"""
        self.clear_screen()     # Clears the screen.
        tk.Label(self.root, text=f"{self.difficulty} Sudoku", font=("Century", 26), bg="#74CDED").pack(pady=(25, 10))

        # Creates a 9x9 matrix (self.entries) to store Tkinter Entry widgets.
        self.entries = [[None for _ in range(9)] for _ in range(9)]

        # Stores predefined tiles in self.static_tiles
        self.static_tiles = set()

        # Creates a frame to hold the Sudoku grid.
        main_frame = tk.Frame(self.root)
        main_frame.pack()

        # Create 9 frames for 3x3 sub-grids
        subgrid_frames = [[tk.Frame(main_frame, borderwidth=4, relief="solid", padx=0, pady=0) for _ in range(3)] for _
                          in range(3)]

        # Position sub-grid frames in a 3x3 layout
        for i in range(3):
            for j in range(3):
                subgrid_frames[i][j].grid(row=i, column=j, sticky="nsew")

        """"
        Create the 9x9 Sudoku grid inside the appropriate subgrid frames
        - If a cell has a number (≠0): Inserts the number. Disables the cell (state="readonly").
        - Changes the background color to "light gray". Marks it as static so algorithm doesn't change it
        """
        for i in range(9):
            for j in range(9):
                value = self.grid[i][j]
                entry = tk.Entry(subgrid_frames[i // 3][j // 3], width=2, font=("Arial", 28), justify="center")
                entry.grid(row=i % 3, column=j % 3, padx=1, pady=1)

                if value != 0:
                    entry.insert(0, str(value))
                    entry.config(state="readonly", disabledbackground="lightgray")
                    self.static_tiles.add((i, j))  # Mark as static tile

                self.entries[i][j] = entry

        # Buttons for Back and Simple and Smart Backtracking
        # Creates a frame for the buttons.
        btn_frame = tk.Frame(self.root, bg="#74CDED")
        btn_frame.pack(pady=10)

        # Back - Returns to the welcome screen.
        tk.Button(btn_frame, text="← Back", font=("Arial", 16),
                  command=self.create_welcome_screen).pack(side="left",padx=5)
        # Simple Backtracking - Calls solve_simple()
        tk.Button(btn_frame, text="Simple Backtracking",
                  font=("Arial", 16), command=self.solve_simple).pack(side="left", padx=5)
        # Smart Backtracking - Calls solve_smart().
        tk.Button(btn_frame, text="Smart Backtracking", font=("Arial", 16), command=self.solve_smart).pack(side="left", padx=5)

    def solve_simple(self):
        """Solve Sudoku using basic backtracking"""
        self.solve_sudoku(lambda csp: backtracking_search(csp), self.difficulty, "Simple")


    def solve_smart(self):
        """Solve Sudoku using smart backtracking with MRV, LCV, and Forward Checking"""
        self.solve_sudoku(
            lambda csp: backtracking_search(
                csp,
                select_unassigned_variable=mrv,     # MRV for variable selection
                order_domain_values=lcv,            # LCV for value ordering
                inference=forward_checking          # Forward Checking for inference
            ),
            self.difficulty, "Smart"
        )


    def solve_sudoku(self, solver, difficulty, solver_type):
        """Execute the selected solver method and display the solution"""
        sudoku = Sudoku(self.grid)  # Initialize Sudoku CSP
        start_time = time.time()
        solution, correct_assignments, incorrect_assignments, total_assignments = solver(sudoku)
        elapsed_time = round((time.time() - start_time) * 1000, 2)  # Converted to milliseconds

        if solution:
            for i in range(9):
                for j in range(9):
                    if (i, j) not in self.static_tiles:  # Only update empty cells
                        self.entries[i][j].delete(0, "end")
                        self.entries[i][j].insert(0, str(solution[(i, j)]))
                        self.entries[i][j].config(state="readonly", disabledbackground="lightblue")

            messagebox.showinfo(
                f"{difficulty} Sudoku Solved!",
                f"Solved with {solver_type} Backtracking\n"
                f"Solved in {elapsed_time} ms!\n"
                f"Correct Assignments: {correct_assignments}\n"
                f"Incorrect Assignments (Backtracking Steps): {incorrect_assignments}\n"
                f"Total Assignments: {total_assignments}"
            )
        else:
            messagebox.showerror(f"{difficulty} - {solver_type} Backtracking", "No solution found!")



    def clear_screen(self):
        """Remove all widgets before changing screens"""
        for widget in self.root.winfo_children():
            widget.destroy()


# Run the Application
root = tk.Tk()
app = SudokuGUI(root)
root.mainloop()
