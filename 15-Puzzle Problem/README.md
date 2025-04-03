# Homework Assignment 1: The 15-Puzzle Problem Solver
## CS 580: Introduction to Artificial Intelligence
**Author** Sahad Rafiuzzaman
**Date:** 01/26/2025

## Overview
This project is a graphical 15-Puzzle Problem solver built using Python (Tkinter). It applies three different search 
algorithms to solve the puzzle and selects the best one based on time, memory usage, and nodes expanded.

This project is based on the original eight_puzzle.py code from the AIMA 
(Artificial Intelligence: A Modern Approach) library.

## Features
* Graphical User Interface using Tkinter.
* Scramble the puzzle to generate a new challenging experience.
* Three Search Algorithms:
  * A* Search (Informed Heuristic Search)
  * Breadth-First Graph Search (BFS)
  * Iterative Deepening Search (IDDFS)
* Compare metrics and performances
  * Number of nodes expanded.
  * Time taken to solve the puzzle.
  * Memory usage.
* Selects the best algorithm based on performance.

## Installation
Be sure to have Python installed along with the following libraries:
* tkinter (for GUI)
* tracemalloc (for memory tracking)
* time (for runtime measurement)
* random (for scrambling the puzzle)

## How to Run
Run the following command to start the 15-Puzzle Solver GUI:
python fifteen_puzzle.py

This will launch the Tkinter window, where you can:
* Scramble = Scramble the puzzle.
* Check Algorithms = Compare different algorithms.
* Solve = Solve the puzzle using the best search algorithm.

## How it Works
1. Click the Scramble button to shuffle the puzzle tiles randomly.
2. Click the Check Algorithms button to compare the search strategies. It will print the moves, time taken, memory used,
and nodes expanded for each algorithm.
3. Click the solve button to let the best algorithm find the solution.

## File Structure
1. Main.py
2. fifteen_search.py
3. utils.py
4. README.md
5. Future Revision.png
6. 15-Puzzle Problem Analysis Report.pdf
7. 15-Puzzle Problem Instructions.pdf

## Acknowledgments
* Based on AIMA Python Code: https://github.com/aimacode
* Learned Tkinter from Codemy.com: https://www.youtube.com/@Codemycom