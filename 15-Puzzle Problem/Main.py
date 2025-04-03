# Sahad Rafiuzzaman
# Date: 01/26/2025
# CS 580: Introduction to Artificial Intelligence
# Homework Assignment 1: The 15-Puzzle Problem

# This homework assignment is built on the original eight_puzzle.py code from the AIMA library.
# It uses a graphical interface (Tkinter) for solving the 15-puzzle problem using three search algorithms: A* Search
# (Informed Heuristic Search), Breadth First Graph Search (BFS), and Iterative Deepening Search (IDDFS).
# The program prints out selects the most effective algorithm based on nodes expanded, runtime, and memory usage.

import os.path
import random
import time
from functools import partial
from tkinter import *
from fifteen_search import FifteenPuzzle, astar_search, breadth_first_graph_search, iterative_deepening_search
import tracemalloc      # Tracks memory usage for performance comparison

# Initialize the main GUI window
root = Tk()
root.title("15-Puzzle Problem")

# Create the puzzle display frame
puzzle_frame = LabelFrame(root, text="Puzzle", padx=10, pady=10)
puzzle_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="nsew")

# Initialize the solved puzzle state
state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
puzzle = FifteenPuzzle(tuple(state))
solution = None
b = [None] * 16


def scramble():
    """Randomly scrambles the puzzle state to generate a solvable puzzle."""
    global state, puzzle
    possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    # Perform 60 random valid moves to scramble the puzzle
    scramble_moves = [random.choice(possible_actions) for _ in range(60)]

    for move in scramble_moves:
        if move in puzzle.actions(state):
            state = list(puzzle.result(state, move))
            puzzle = FifteenPuzzle(tuple(state))
            puzzle_tiles()  # Update the GUI


def puzzle_tiles():
    """Updates the puzzle tiles based on the current puzzle state. Creates dynamic buttons."""
    for i in range(16):
        row, col = divmod(i, 4)     # Convert index to (row, col)
        b[i] = Button(puzzle_frame, text=f'{state[i]}' if state[i] != 0 else None, width=6,
                      font=('Helvetica', 40, 'bold'), command=partial(exchange, i))
        b[i].grid(row=row, column=col, ipady=40)

def exchange(index):
    """Interchanges the position of the selected tile with the zero tile under certain conditions"""

    global state, solution, puzzle
    zero_ix = list(state).index(0)

    # Determine the direction of movement
    actions = puzzle.actions(state)
    current_action = ''
    i_diff = index // 4 - zero_ix // 4
    j_diff = index % 4 - zero_ix % 4
    if i_diff == 1:
        current_action += 'DOWN'
    elif i_diff == -1:
        current_action += 'UP'
    elif j_diff == 1:
        current_action += 'RIGHT'
    elif j_diff == -1:
        current_action += 'LEFT'

    # Ensure the move is valid
    if abs(i_diff) + abs(j_diff) != 1:
        current_action = ''

    if current_action in actions:
        b[zero_ix].grid_forget()
        b[zero_ix] = Button(puzzle_frame, text=f'{state[index]}', width=6, font=('Helvetica', 40, 'bold'),
                            command=partial(exchange, zero_ix))
        b[zero_ix].grid(row=zero_ix // 4, column=zero_ix % 4, ipady=40)
        b[index].grid_forget()
        b[index] = Button(puzzle_frame, text=None, width=6, font=('Helvetica', 40, 'bold'), command=partial(exchange, index))
        b[index].grid(row=index // 4, column=index % 4, ipady=40)
        state[zero_ix], state[index] = state[index], state[zero_ix]
        puzzle = FifteenPuzzle(tuple(state))

def command_buttons():
    """Creates the buttons for scrambling, solving, and checking algorithms."""
    command_frame = LabelFrame(root, text="Button", padx=10, pady=10)
    command_frame.grid(row=3, column=4, rowspan=4, sticky="nsew")

    # Scramble button
    scramble_button = Button(command_frame, text='Scramble', font=('Helvetica', 18, 'bold'), width=16, command=init)
    scramble_button.grid(row=0, column=0, ipady=5, pady=10, sticky='ew')

    # Check algorithm performance button
    check_btn = Button(command_frame, text='Check Algorithms', font=('Helvetica', 18, 'bold'), width=16, command=output_results)
    check_btn.grid(row=1, column=0, ipady=5, pady=10, sticky='ew')

    # Solve using the best algorithm button
    solve_btn = Button(command_frame, text='Solve', font=('Helvetica', 18, 'bold'), width=16, command=solve_best)
    solve_btn.grid(row=2, column=0, ipady=5, pady=10, sticky='ew')

def output_results():
    # Solve using Informed Heuristic Search (A*)
    solution_ihs, total_time_ms_ihs, memory_usage_kb_ihs, nodes_expanded_ihs = solve_IHS()
    formatted_moves_ihs = ''.join(move[0] for move in solution_ihs)
    solution_exists_ihs = bool(solution_ihs)

    print("\nSearching Strategy: Informed Heuristic Search (IHS)")
    print(f"Moves: {formatted_moves_ihs}")
    print(f"Nodes Expanded: {nodes_expanded_ihs}")
    print(f"Time Taken: {total_time_ms_ihs:.1f} ms")
    print(f"Memory Used: {memory_usage_kb_ihs:.1f} KB")
    print(f"Solution Exists: {solution_exists_ihs}")

    # Solve using Breadth-First Search (BFS)
    solution_bfs, total_time_ms_bfs, memory_usage_kb_bfs, nodes_expanded_bfs = solve_BFS()
    formatted_moves_bfs = ''.join(move[0] for move in solution_bfs)
    solution_exists_bfs = bool(solution_bfs)

    print("\nSearching Strategy: Breadth-First Graph Search (BFS)")
    print(f"Moves: {formatted_moves_bfs}")
    print(f"Nodes Expanded: {nodes_expanded_bfs}")
    print(f"Time Taken: {total_time_ms_bfs:.1f} ms")
    print(f"Memory Used: {memory_usage_kb_bfs:.1f} KB")
    print(f"Solution Exists: {solution_exists_bfs}")

    # Solve using Iterative Deepening Search (IDDFS)
    solution_iddfs, total_time_ms_iddfs, memory_usage_kb_iddfs, nodes_expanded_iddfs = solve_IDDFS()
    formatted_moves_iddfs = ''.join(move[0] for move in solution_iddfs)
    solution_exists_iddfs = bool(solution_iddfs)

    print("\nSearching Strategy: Iterative Deepening Search (IDDFS)")
    print(f"Moves: {formatted_moves_iddfs}")
    print(f"Nodes Expanded: {nodes_expanded_iddfs}")
    print(f"Time Taken: {total_time_ms_iddfs:.1f} ms")
    print(f"Memory Used: {memory_usage_kb_iddfs:.1f} KB")
    print(f"Solution Exists: {solution_exists_iddfs}")

def solve_IHS():
    """Solves the puzzle using astar_search (Informed Heuristic Search)."""
    tracemalloc.start()
    start_time = time.time()

    solution_node_IHS, nodes_expanded_IHS = astar_search(puzzle, display=True)

    end_time = time.time()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    total_time_ms_IHS = (end_time - start_time) * 1000
    memory_usage_kb_IHS = peak_memory / 1024

    return solution_node_IHS.solution(), total_time_ms_IHS, memory_usage_kb_IHS, nodes_expanded_IHS


def solve_steps_IHS():
    """Solves the puzzle step by step using astar_search (IHS)."""
    global puzzle, solution, state

    solution_IHS, total_time_ms_IHS, memory_usage_kb_IHS, nodes_expanded_IHS = solve_IHS()

    for move in solution_IHS:
        state = puzzle.result(state, move)
        puzzle_tiles()
        root.update()
        root.after(1, time.sleep(0.75))


def solve_BFS():
    """Solves the puzzle using Breadth-First Graph Search (BFS)"""
    tracemalloc.start()
    start_time = time.time()

    solution_node_BFS, nodes_expanded_BFS = breadth_first_graph_search(puzzle)
    end_time = time.time()

    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    total_time_ms_BFS = (end_time - start_time) * 1000
    memory_usage_kb_BFS = peak_memory / 1024

    return solution_node_BFS.solution(), total_time_ms_BFS, memory_usage_kb_BFS, nodes_expanded_BFS


def solve_steps_BFS():
    """Solves the puzzle step by step using Breadth-First Graph Search (BFS)."""
    global puzzle, solution, state

    solution_BFS, total_time_ms_BFS, memory_usage_kb_BFS, nodes_expanded_BFS = solve_BFS()

    for move in solution_BFS:
        state = puzzle.result(state, move)
        puzzle_tiles()
        root.update()
        root.after(1, time.sleep(0.75))


def solve_IDDFS():
    """Solves the puzzle using Iterative Deepening Search (IDDFS)"""
    tracemalloc.start()
    start_time = time.time()

    solution_node_IDDFS, nodes_expanded_IDDFS = iterative_deepening_search(puzzle)
    end_time = time.time()

    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    total_time_ms_IDDFS = (end_time - start_time) * 1000
    memory_usage_kb_IDDFS = peak_memory / 1024

    # Handle case where no solution is found
    if solution_node_IDDFS is None:
        return [], total_time_ms_IDDFS, memory_usage_kb_IDDFS, nodes_expanded_IDDFS

    return solution_node_IDDFS.solution(), total_time_ms_IDDFS, memory_usage_kb_IDDFS, nodes_expanded_IDDFS


def solve_steps_IDDFS():
    """Solves the puzzle step by step using iterative deepening search (IDDFS)."""
    global puzzle, solution, state

    solution_IDDFS, total_time_ms_IDDFS, memory_usage_kb_IDDFS, nodes_expanded_IDDFS = solve_IDDFS()

    for move in solution_IDDFS:
        state = puzzle.result(state, move)
        puzzle_tiles()
        root.update()
        root.after(1, time.sleep(0.75))


def solve_best():
    """Solves the puzzle using the best algorithm based on time, memory, and nodes expanded."""
    global puzzle, state

    # Run all three algorithms and store their results
    results = [solve_IHS(), solve_BFS(), solve_IDDFS()] # (solution, time, memory, nodes)

    # Initialize best values with the first algorithm's result
    best_solution, best_time, best_memory, best_nodes = results[0]

    # Compare with the other algorithms
    for solution, time_taken, memory_used, nodes_expanded in results[1:]:
        if (time_taken < best_time) or \
           (time_taken == best_time and memory_used < best_memory) or \
           (time_taken == best_time and memory_used == best_memory and nodes_expanded < best_nodes):
            best_solution, best_time, best_memory, best_nodes = solution, time_taken, memory_used, nodes_expanded

    # Apply the best solution step by step
    for move in best_solution:
        state = puzzle.result(state, move)
        puzzle_tiles()
        root.update()
        root.after(1, time.sleep(0.75))


def init():
    """Initializes the puzzle, scrambles it, and sets up the GUI controls."""

    global state, solution
    state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

    scramble()
    puzzle_tiles()
    command_buttons()

if __name__ == "__main__":
    init()
    root.mainloop()

