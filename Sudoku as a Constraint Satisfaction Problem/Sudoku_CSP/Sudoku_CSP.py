"""
Sahad Rafiuzzaman
Date: 03/02/2025
CS 580: Introduction to Artificial Intelligence
Homework Assignment 2: Sudoku as a Constraint Satisfaction Problem

This Sudoku_CSP.py file is originally from the csp.py file in the AIMA GitHub Library:
https://github.com/aimacode/aima-python
"""

# Imported necessary libraries
from operator import neg
from sortedcontainers import SortedSet      # pip install sortedcontainers
import search
from utils import argmin_random_tie, count, first


class CSP(search.Problem):
    """
    This class describes finite-domain Constraint Satisfaction Problems.
    A CSP is specified by the following inputs:
    - variables
        - A list of variables; each is atomic (e.g. int or string).
    - domains
        - A dict of {var:[possible_value, ...]} entries.
    - neighbors
        - A dict of {var:[var,...]} that for each variable lists the other variables that participate in constraints.
    - constraints
        - A function f(A, a, B, b) that returns true if neighbors A, B satisfy the constraint when they have values A=a, B=b

    In the textbook and in most mathematical definitions, the constraints are specified as explicit pairs of allowable
    values, but the formulation here is easier to express and more compact for most cases (for example, the n-Queens
    problem can be represented in O(n) space using this notation, instead of O(n^4) for the explicit representation).
    In terms of describing the CSP as a problem, that's all there is.

    However, the class also supports data structures and methods that help you solve CSPs by calling a search function
    on the CSP. Methods and slots are as follows, where the argument 'a' represents an assignment, which is a
    dict of {var:val} entries:
        - assign(var, val, a)       Assign a[var] = val; do other bookkeeping
        - unassign(var, a)          Do del a[var], plus other bookkeeping
        - nconflicts(var, val, a)   Return the number of other variables that conflict with var=val
        - curr_domains[var]         Slot: remaining consistent values for var used by constraint propagation routines.

    The following methods are used only by graph_search and tree_search:
        - actions(state)          Return a list of actions
        - result(state, action)   Return a successor of state
        - goal_test(state)        Return true if all constraints satisfied

    The following are just for debugging purposes:
        nassigns                Slot: tracks the number of assignments made
        display(a)              Print a human-readable representation
    """

    def __init__(self, variables, domains, neighbors, constraints):
        """Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
        super().__init__(())
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = None
        self.nassigns = 0

    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""

        # Subclasses may implement this more efficiently
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])

        return count(conflict(v) for v in self.neighbors[var])

    def display(self, assignment):
        """Show a human-readable representation of the CSP."""
        # Subclasses can print in a prettier way, or display with a GUI
        print(assignment)

    def actions(self, state):
        """Return a list of applicable actions: non conflicting
        assignments to an unassigned variable."""
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
            return [(var, val) for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]

    def result(self, state, action):
        """Perform an action and return the new state."""
        (var, val) = action
        return state + ((var, val),)

    def goal_test(self, state):
        """The goal is to assign all variables, with all constraints satisfied."""
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))


    # These are for constraint propagation

    def support_pruning(self):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        """Rule out var=value."""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        """Return the partial assignment implied by the current inferences."""
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)

    # This is for min_conflicts search

    def conflicted_vars(self, current):
        """Return a list of variables in current assignment that are in conflict"""
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]

# ______________________________________________________________________________

class Sudoku(CSP):
    """
    Sudoku CSP
    - Variables: Each empty cell in the 9x9 Sudoku grid.
    - Domains: Possible values (1-9) for each variable.
    - Constraints: Ensure that no two identical numbers appear in the same row, column, or 3x3 sub-grid
    """
    def __init__(self, grid):
        """Initialize the Sudoku as a Constraint Satisfaction Problem (CSP)."""
        self.grid = grid

        # Define all variables (both assigned and unassigned)
        variables = [(i, j) for i in range(9) for j in range(9)]

        # Define initial domains (1-9 for empty cells, fixed for pre-filled)
        domains = {}
        for i in range(9):
            for j in range(9):
                if grid[i][j] != 0:
                    domains[(i, j)] = [grid[i][j]]
                else:
                    domains[(i, j)] = list(range(1, 10))

        # Reduce domains based on existing values in rows, columns, and sub-grids
        for var in variables:
            row, col = var
            if grid[row][col] == 0:
                used_numbers = set(self.get_neighbors_values(row, col))
                domains[var] = [num for num in domains[var] if num not in used_numbers]

        # Define constraints: all variables in the same row, column, or sub-grid
        neighbors = {var: self.get_neighbors(*var) for var in variables}

        # Initialize CSP with variables, domains, neighbors, and constraints
        CSP.__init__(self, variables, domains, neighbors, self.constraint)

    def get_neighbors(self, row, col):
        """Find all neighbors (same row, column, or 3x3 sub-grid)."""
        neighbors = set()

        # Row & Column Neighbors
        for i in range(9):
            if i != col:
                neighbors.add((row, i))  # Same row
            if i != row:
                neighbors.add((i, col))  # Same column

        # Sub-grid Neighbors
        box_row, box_col = row // 3 * 3, col // 3 * 3  # Identify 3x3 grid start
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if (i, j) != (row, col):
                    neighbors.add((i, j))

        return neighbors

    def get_neighbors_values(self, row, col):
        """Return the values of assigned neighbors (row, column, sub-grid)."""
        neighbors = self.get_neighbors(row, col)
        return [self.grid[r][c] for r, c in neighbors if self.grid[r][c] != 0]

    def constraint(self, A, a, B, b):
        """Constraint function: No two neighboring variables can have the same value."""
        return a != b

# ______________________________________________________________________________

# Constraint Propagation with AC3

def dom_j_up(csp, queue):
    return SortedSet(queue, key=lambda t: neg(len(csp.curr_domains[t[1]])))

def revise(csp, Xi, Xj, removals, checks=0):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
        conflict = True
        for y in csp.curr_domains[Xj]:
            if csp.constraints(Xi, x, Xj, y):
                conflict = False
            checks += 1
            if not conflict:
                break
        if conflict:
            csp.prune(Xi, x, removals)
            revised = True
    return revised, checks

# Constraint Propagation with AC3b: an improved version of AC3 with double-support domain-heuristic

def AC3b(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        # Si_p values are all known to be supported by Xj
        # Sj_p values are all known to be supported by Xi
        # Dj - Sj_p = Sj_u values are unknown, as yet, to be supported by Xi
        Si_p, Sj_p, Sj_u, checks = partition(csp, Xi, Xj, checks)
        if not Si_p:
            return False, checks  # CSP is inconsistent
        revised = False
        for x in set(csp.curr_domains[Xi]) - Si_p:
            csp.prune(Xi, x, removals)
            revised = True
        if revised:
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
        if (Xj, Xi) in queue:
            if isinstance(queue, set):
                # or queue -= {(Xj, Xi)} or queue.remove((Xj, Xi))
                queue.difference_update({(Xj, Xi)})
            else:
                queue.difference_update((Xj, Xi))
            # the elements in D_j which are supported by Xi are given by the union of Sj_p with the set of those
            # elements of Sj_u which further processing will show to be supported by some vi_p in Si_p
            for vj_p in Sj_u:
                for vi_p in Si_p:
                    conflict = True
                    if csp.constraints(Xj, vj_p, Xi, vi_p):
                        conflict = False
                        Sj_p.add(vj_p)
                    checks += 1
                    if not conflict:
                        break
            revised = False
            for x in set(csp.curr_domains[Xj]) - Sj_p:
                csp.prune(Xj, x, removals)
                revised = True
            if revised:
                for Xk in csp.neighbors[Xj]:
                    if Xk != Xi:
                        queue.add((Xk, Xj))
    return True, checks  # CSP is satisfiable

def partition(csp, Xi, Xj, checks=0):
    Si_p = set()
    Sj_p = set()
    Sj_u = set(csp.curr_domains[Xj])
    for vi_u in csp.curr_domains[Xi]:
        conflict = True
        # now, in order to establish support for a value vi_u in Di it seems better to try to find a support among
        # the values in Sj_u first, because for each vj_u in Sj_u the check (vi_u, vj_u) is a double-support check
        # and it is just as likely that any vj_u in Sj_u supports vi_u than it is that any vj_p in Sj_p does...
        for vj_u in Sj_u - Sj_p:
            # double-support check
            if csp.constraints(Xi, vi_u, Xj, vj_u):
                conflict = False
                Si_p.add(vi_u)
                Sj_p.add(vj_u)
            checks += 1
            if not conflict:
                break
        # ... and only if no support can be found among the elements in Sj_u, should the elements vj_p in Sj_p be used
        # for single-support checks (vi_u, vj_p)
        if conflict:
            for vj_p in Sj_p:
                # single-support check
                if csp.constraints(Xi, vi_u, Xj, vj_p):
                    conflict = False
                    Si_p.add(vi_u)
                checks += 1
                if not conflict:
                    break
    return Si_p, Sj_p, Sj_u - Sj_p, checks

# ______________________________________________________________________________

# CSP Backtracking Search

# Variable ordering
def first_unassigned_variable(assignment, csp):
    """The default variable order."""
    return first([var for var in csp.variables if var not in assignment])


def mrv(assignment, csp):
    """Minimum-remaining-values heuristic."""
    return argmin_random_tie([v for v in csp.variables if v not in assignment],
                             key=lambda var: num_legal_values(csp, var, assignment))

def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count(csp.nconflicts(var, val, assignment) == 0 for val in csp.domains[var])


# Value ordering

def unordered_domain_values(var, assignment, csp):
    """The default value order."""
    return csp.choices(var)


def lcv(var, assignment, csp):
    """Least Constraining Value heuristic.
    Returns values sorted by the number of conflicts they cause for neighbors.
    """
    return sorted(csp.domains[var], key=lambda val: count(
        not csp.constraints(var, val, neighbor, b)
        for neighbor in csp.neighbors[var]
        for b in csp.domains[neighbor]
    ))


# Inference

def no_inference(csp, var, value, assignment, removals):
    return True

def forward_checking(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                return False
    return True

# The search, proper
def backtracking_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, inference=no_inference):
    """
    Solves a Constraint Satisfaction Problem (CSP) using Backtracking Search.

    This function recursively assigns values to variables while ensuring constraints are met.
    If a conflict occurs, it backtracks and tries different values.

    Parameters:
    - csp: The CSP problem to be solved.
    - select_unassigned_variable: Function to select the next variable to assign (default: first unassigned variable).
    - order_domain_values: Function to determine the order of values to try (default: unordered values).
    - inference: Function to perform constraint propagation (default: no inference).

    Returns:
    - solution (dict): A valid assignment of variables if a solution is found, otherwise None.
    - correct_assignments (int): The number of successful assignments made.
    - incorrect_assignments (int): The number of failed assignments made.
    - total_assignments (int): Total number of assignments attempted (both correct and incorrect).
    """

    def backtrack(assignment, correct_assignments, incorrect_assignments):
        # If all variables are assigned, return solution and counts.
        if len(assignment) == len(csp.variables):
            return assignment, correct_assignments, incorrect_assignments

        # Select the next variable to assign based on the chosen algorithm.
        var = select_unassigned_variable(assignment, csp)

        # Try each possible value from the domain, ordered by the chosen algorithm.
        for value in order_domain_values(var, assignment, csp):
            # Checking if assigning this value would cause a conflict.
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)      # Assign the value.
                correct_assignments += 1                # Increment the correct assignment count.
                # print(f"Assigned {value} to {var}, Correct Assignments: {correct_assignments}")   # Debugging

                # Save the current state before making inferences.
                removals = csp.suppose(var, value)

                # Perform constraint.
                if inference(csp, var, value, assignment, removals):
                    # Attempt to solve the rest of the problem.
                    result, correct_count, incorrect_count = backtrack(
                        assignment,
                        correct_assignments,
                        incorrect_assignments
                    )
                    # If a valid solution is found, return it.
                    if result is not None:
                        return result, correct_count, incorrect_count  # Always return 3 values

                # If backtracking occurs, restore previous state.
                csp.restore(removals)

            incorrect_assignments += 1  # Increment incorrect assignment count.
            # print(f"Assigned {value} to {var}, incorrect Assignments: {incorrect_assignments}")   # Debugging

        # If no valid assignment was found for this variable, remove it and backtrack
        csp.unassign(var, assignment)
        return None, correct_assignments, incorrect_assignments

    # Start the backtracking process with an empy assignment and initial counts
    result, correct_assignments, incorrect_assignments = backtrack({}, 0, 0)

    # Verify the final result meets the CSP constraints
    assert result is None or csp.goal_test(result)

    # Compute the total number of attempted assignments (successful + failed)
    total_assignments = correct_assignments + incorrect_assignments

    # Return the solution along with performance metrics
    return result, correct_assignments, incorrect_assignments, total_assignments  # Always return 4 values







