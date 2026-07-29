# Sahad Rafiuzzaman
# Date: 04/24/2025
# CS 580: Introduction to Artificial Intelligence
# Homework Assignment 4: Decision Tree Classifier using Methods

"""
Description:
This program implements a Decision Tree classifier from scratch to predict whether a car is "profitable" or not,
based on four attributes: price, maintenance, capacity, and airbag.
Assuming that all foru attributes are categorical with discrete values.
"""

"""
Datasets:
"trainData" contains the data to be trained on.
"testData" contains the data on which the model will be tested on.
"""

"""
Task A
Train the decision tree classifier on the trainData using any tow of the following methods:
1. Random
2. Least-Value
3. Most-Value
4. Gini index
5. Information Gain

The selected methods must work to build a decision tree. Test the model on testData. After predictions, report the 
individual accuracies on the test data. Note that the "profitable" field should not be used in the 
classification process.
"""

"""
Task B
The program prints the decision tree using indentation to represent different levels of the tree.

Each split shows the attribute and its corresponding value, followed by a colon and the decision (yes or no)
when a leaf node is reached. Indentation increases with each deeper level of the tree.

Example format:
If the root node splits on 'price', and the next level splits on 'maintenance', and then on 'capacity',
the output will look like this:

price = low
| maintenance = low
| | capacity = 4 : yes
| maintenance = high : no
price = high
| ...

This format must be used to visualize the logic of the decision tree clearly, with each level shown
by an increasing number of indentation markers ('|    ').
"""

"""
Task C (Extra Credit)

This program implements both Information Gain and Gini Index to determine the best attribute for splitting at each node.
Using one of these methods earns 10 extra points. Using both earns a total of 20 extra points.

To understand how these attribute selection methods work, you can refer to the example and explanation provided here:
https://www.bogotobogo.com/python/scikit-learn/scikt_machine_learning_Decision_Tree_Learning_Informatioin_Gain_IG_Impurity_Entropy_Gini_Classification_Error.php
"""

"""
Sources:
https://stockcake.com/i/colorful-decision-tree_578600_1040538
https://www.youtube.com/watch?v=WurCpmHtQc4&ab_channel=Codemy.com
"""

# ---------- Importing Necessary Libraries ---------- #
import pandas as pd
import random
import math
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, scrolledtext

# ---------- Load Training and Testing data ---------- #
def load_data(train_path, test_path):
    train_df = pd.read_csv(train_path)                          # Reading the trainData.csv
    test_df = pd.read_csv(test_path)                            # Reading the testData.csv
    train_df["capacity"] = train_df["capacity"].astype(str)     # Convert "capacity" into a categorical attribute
    test_df["capacity"] = test_df["capacity"].astype(str)       # Convert "capacity" into a categorical attribute
    return train_df, test_df

# ---------- Reading the data from the CSV files ---------- #
# Load the training and testing datasets from CSV files using the load_data function
train_df, test_df = load_data("trainData.csv", "testData.csv")
# Convert the training data into a list of lists for easier processing
train_data = train_df.values.tolist()
# Convert the test data into a list of dictionaries
test_data = test_df.to_dict(orient="records")
# Get the list of column names except the last one
attributes = list(train_df.columns[:-1])

# ---------- Outputting Data ---------- #
# Print the number of rows and columns in the training and test datasets
print(f'Train Data Shape: {train_df.shape}')
print(f'Test Data Shape: {test_df.shape}')

# Show the first 10 rows of the training data to get a quick look at it
print(f'\nTop 10 rows of Train Data:\n{train_df.head(10)}')

# Show the first 10 rows of the test data to get a quick look at it
print(f'\nTop 10 rows of Test Data:\n{test_df.head(10)}\n')

# Loop through each column in the training data (except the last one)
for index in range(len(train_df.columns) - 1):
    col_name = train_df.columns[index]                      # Get the column name
    unique_vals = train_df[col_name].unique()               # Get unique values in that column
    # Print how many unique values and what they are
    print(f"{col_name}: {len(unique_vals)} unique values → {list(unique_vals)}")


# ---------- Basic Tree Functions ---------- #
# Finds the most common class label (like 'yes' or 'no') in the given data
def majority_class(data):
    labels = [row[-1] for row in data]                      # Get the last item in each row (the label)
    return max(set(labels), key=labels.count)               # Return the label that appears the most

# Checks if all the rows in the dataset have the same class label
def is_pure(data):
    return all(row[-1] == data[0][-1] for row in data)      # True if all labels are the same

# Builds a list of strings that show the structure of the decision tree
def print_tree(tree, indent=""):
    lines = []                                              # Store each line of the printed tree
    if isinstance(tree, str):
        lines.append(indent + tree)                         # Just add the class label if it's a leaf
    else:
        for (attr, value), subtree in sorted(tree.items()):  # Go through each branch
            line = f"{indent}{attr} = {value}"
            if isinstance(subtree, str):                    # If it's a leaf, show the result
                lines.append(line + " : " + subtree.strip(" :"))
            else:
                lines.append(line)                          # Add the current condition
                lines += print_tree(subtree, indent + "|    ")  # Recursively print the subtree
    return lines                                               # Return all lines to be printed

# Makes a prediction for one row by following the decision tree
def predict(tree, row):
    print("\n")                                             # Print a newline to separate outputs
    while isinstance(tree, dict):                           # Keep going while we're still in a tree node
        found = False
        for (attr, value), subtree in tree.items():
            print(f"Testing attribute: {attr}, expected value: {value}, actual value: {row.get(attr)}")
            if attr in row and row[attr] == value:
                tree = subtree                              # Move to the next branch of the tree
                found = True
                break
        if not found:                                   # If no match is found, guess using the most common class
            return majority_class([list(row.values()) + ["yes"], list(row.values()) + ["no"]])
    return tree.strip(" :")                                 # Return the predicted class label

# Tests the tree on the test data and calculates the accuracy
def evaluate(tree, test_data):
    correct = 0                                         # Keep track of how many predictions are correct
    log = []                                            # Store the prediction results
    for row in test_data:
        actual = row["profitable"]                      # The actual label
        pred = predict(tree, row)                       # What the tree predicted
        log.append(f"Predicted: {pred}, Actual: {actual}\n")
        if pred == actual:
            correct += 1
    accuracy = correct / len(test_data)                 # Calculate how many were right
    log.append(f"Accuracy: {accuracy * 100:.2f}%")      # Add accuracy to the log
    return "".join(log)                                 # Return the whole log as one string


# ---------- Random Method ---------- #
random_order = []  # This list keeps track of the order in which attributes are picked

def build_tree_random(data, attributes_left):
    # If all labels are the same or no attributes are left, return the majority label
    if is_pure(data) or not attributes_left:
        return " : " + majority_class(data)

    # Pick a random attribute from the list
    index = random.randint(0, len(attributes_left) - 1)
    attr_name = attributes_left[index]

    # Save the chosen attribute if not already saved
    if attr_name not in random_order:
        random_order.append(attr_name)

    # Find the index of the attribute in the dataset
    attr_index = train_df.columns.get_loc(attr_name)

    # Get all possible values of this attribute
    values = sorted(set(row[attr_index] for row in data))
    tree = {}

    # Make a new attribute list without the chosen one
    new_attrs = attributes_left[:index] + attributes_left[index+1:]

    # For each value of the attribute, build a subtree
    for value in values:
        subset = [row for row in data if row[attr_index] == value]
        tree[(attr_name, value)] = build_tree_random(subset, new_attrs) if subset else " : " + majority_class(data)

    return tree

# ---------- Least-Value Method ---------- #
def best_split_least_values(dataset, attrs):
    min_values = float("inf")  # Start with a very large number
    candidates = []  # This will store attributes with the smallest number of unique values

    for attr in attrs:
        index = train_df.columns.get_loc(attr)
        unique_vals = set(row[index] for row in dataset)
        val_count = len(unique_vals)

        # If this attribute has fewer values, it's a better candidate
        if val_count < min_values:
            min_values = val_count
            candidates = [attr]
        elif val_count == min_values:
            candidates.append(attr)

    # Pick randomly among the best candidates
    return random.choice(candidates) if candidates else None

least_order = []  # Keeps track of the order of selected attributes for Least-Value method

def build_tree_least(data, attrs):
    # If pure or no more attributes, return the majority label
    if is_pure(data) or not attrs:
        return " : " + majority_class(data)

    # Choose the attribute with the fewest unique values
    best_attr = best_split_least_values(data, attrs)

    # Save the attribute order
    if best_attr not in least_order:
        least_order.append(best_attr)

    # Get the index of the chosen attribute
    index = train_df.columns.get_loc(best_attr)

    # Get all the unique values for that attribute
    values = sorted(set(row[index] for row in data))
    tree = {}

    # Remove the used attribute from the list
    new_attrs = [a for a in attrs if a != best_attr]

    # For each value, build a subtree
    for value in values:
        subset = [row for row in data if row[index] == value]
        tree[(best_attr, value)] = build_tree_least(subset, new_attrs) if subset else " : " + majority_class(data)
    return tree


# ---------- Most-Value Method ---------- #
# This function finds the attribute with the most different values
def best_split_most_values(dataset, attrs):
    max_values = float("-inf")  # Start with the smallest number possible
    candidates = []  # Store attributes with the most values

    for attr in attrs:
        index = train_df.columns.get_loc(attr)
        unique_vals = set(row[index] for row in dataset)
        val_count = len(unique_vals)

        # Save the attribute if it has more values
        if val_count > max_values:
            max_values = val_count
            candidates = [attr]
        elif val_count == max_values:
            candidates.append(attr)

    # Randomly pick one if there's a tie
    return random.choice(candidates) if candidates else None

most_order = []  # Keeps track of the order of selected attributes

# This function builds the decision tree using the most-value method
def build_tree_most(data, attrs):
    if is_pure(data) or not attrs:
        return " : " + majority_class(data)

    best_attr = best_split_most_values(data, attrs)
    if best_attr not in most_order:
        most_order.append(best_attr)

    index = train_df.columns.get_loc(best_attr)
    values = sorted(set(row[index] for row in data))
    tree = {}
    new_attrs = [a for a in attrs if a != best_attr]

    for value in values:
        subset = [row for row in data if row[index] == value]
        tree[(best_attr, value)] = build_tree_most(subset, new_attrs) if subset else " : " + majority_class(data)

    return tree

# ---------- Gini Index Method ---------- #
# This function calculates the Gini score, which shows how mixed the labels are
def gini_index(groups, classes):
    total_instances = sum(len(group) for group in groups)
    gini = 0.0

    for group in groups:
        size = len(group)
        if size == 0:
            continue

        score = 0.0
        labels = [row[-1] for row in group]
        for class_val in classes:
            p = labels.count(class_val) / size
            score += p * p

        gini += (1.0 - score) * (size / total_instances)
    return gini

# This function picks the best attribute based on the lowest Gini score
def best_split_gini(dataset, attrs, current_depth):
    class_values = list(set(row[-1] for row in dataset))
    best_attr = None
    lowest_gini = float("inf")

    print(f"\nGini Index for each attribute at depth {current_depth}:")

    for attr in attrs:
        index = train_df.columns.get_loc(attr)
        values = set(row[index] for row in dataset)
        groups = [[row for row in dataset if row[index] == value] for value in values]

        gini = gini_index(groups, class_values)
        print(f"{gini:.4f} {attr}")

        if gini < lowest_gini:
            lowest_gini = gini
            best_attr = attr

    print(f"⮕ Selected: {best_attr}")
    return best_attr

gini_order = []  # Keeps track of which attributes were picked in order

# This function builds the decision tree using the Gini Index method
def build_tree_gini(data, attrs, depth=0):
    if is_pure(data) or not attrs:
        return majority_class(data)

    best_attr = best_split_gini(data, attrs, depth)
    if best_attr not in gini_order:
        gini_order.append(best_attr)

    index = train_df.columns.get_loc(best_attr)
    values = sorted(set(row[index] for row in data))
    tree = {}
    new_attrs = [a for a in attrs if a != best_attr]

    for value in values:
        subset = [row for row in data if row[index] == value]
        tree[(best_attr, value)] = build_tree_gini(subset, new_attrs, depth + 1) if subset else majority_class(data)
    return tree


# ---------- Information Gain Method ---------- #
# This function calculates entropy, which tells us how mixed or messy the labels are
# If all the labels are the same, entropy is 0 (pure)
# If the labels are half yes and half no, entropy is high (very mixed)
def entropy(labels):
    total = len(labels)  # Count how many labels we have
    counts = {}  # Dictionary to count each label
    for label in labels:
        counts[label] = counts.get(label, 0) + 1  # Count how many times each label shows up
    # Calculate entropy using the formula
    return -sum((count / total) * math.log2(count / total) for count in counts.values())

# This function finds the best attribute to split the data
# It chooses the one that gives the most information gain (biggest drop in entropy)
def best_split_info_gain(dataset, attrs, current_depth):
    # First, calculate the entropy before splitting
    base_entropy = entropy([row[-1] for row in dataset])
    best_attr = None  # This will store the best attribute we find
    best_gain = float("-inf")  # Start with the lowest possible gain

    # Print the base entropy for this level of the tree
    print(f"\nInformation Gain for each attribute at depth {current_depth}:")
    print(f"Base Entropy of dataset: {base_entropy:.4f}")

    # Try every attribute one by one
    for attr in attrs:
        index = train_df.columns.get_loc(attr)  # Get the column number
        values = set(row[index] for row in dataset)  # All possible values for this attribute
        weighted_entropy = 0  # This will hold the total entropy after splitting

        # Split the dataset by each value of this attribute
        for value in values:
            subset = [row for row in dataset if row[index] == value]
            prob = len(subset) / len(dataset)  # Probability of this value
            ent = entropy([row[-1] for row in subset])  # Entropy of the subset
            weighted_entropy += prob * ent  # Add to the total weighted entropy

        # Calculate the information gain from this attribute
        gain = base_entropy - weighted_entropy
        print(f"{gain:.4f} {attr}")  # Show gain for this attribute

        # Update the best attribute if this one has a higher gain
        if gain > best_gain:
            best_gain = gain
            best_attr = attr

    print(f"⮕ Selected: {best_attr}")  # Print the best choice
    return best_attr  # Return the attribute with the highest gain

# This list keeps track of the order in which attributes were chosen
info_gain_order = []

# This function builds a decision tree using information gain
def build_tree_info_gain(data, attrs, depth=0):
    # If the data is pure (same label) or there are no more attributes left, stop
    if is_pure(data) or not attrs:
        return majority_class(data)  # Return the most common label

    # Choose the best attribute to split on
    best_attr = best_split_info_gain(data, attrs, depth)
    if best_attr not in info_gain_order:
        info_gain_order.append(best_attr)  # Remember the attribute we used

    index = train_df.columns.get_loc(best_attr)  # Get column index
    values = sorted(set(row[index] for row in data))  # Get all unique values
    tree = {}  # This will hold our decision tree
    new_attrs = [a for a in attrs if a != best_attr]  # Remove the used attribute

    # Build branches of the tree for each value of the best attribute
    for value in values:
        subset = [row for row in data if row[index] == value]
        if subset:
            # Keep building the tree with the remaining attributes
            tree[(best_attr, value)] = build_tree_info_gain(subset, new_attrs, depth + 1)
        else:
            # If there’s no data, return the most common label from the parent
            tree[(best_attr, value)] = majority_class(data)
    return tree  # Return the full tree


# ---------- Using Tkinter to create a GUI ---------- #
class DecisionTreeGUI:
    def __init__(self):
        # A dictionary that connects method names to their tree-building functions
        self.METHODS = {
            "Random": build_tree_random,
            "Least-Values": build_tree_least,
            "Most-Values": build_tree_most,
            "Gini Index": build_tree_gini,
            "Information Gain": build_tree_info_gain
        }

        # Create the main application window
        self.root = tk.Tk()
        self.root.title("Assignment 4: Decision Tree Classifier")  # Title of the window
        self.root.geometry("750x750")  # Set window size
        self.root.resizable(False, False)  # Prevent resizing

        # Load and resize a background image for display
        bg_image = Image.open("Decision_Tree_Image.jpg").resize((600, 600))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a canvas area where we draw everything
        self.canvas = tk.Canvas(self.root, width=750, height=750, bg="#FEFEFE")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(75, 75, image=self.bg_photo, anchor="nw")

        # Create two variables to store the user's dropdown choices
        self.method_var1 = tk.StringVar(value="⮟ Select First Method")
        self.method_var2 = tk.StringVar(value="⮟ Select Second Method")

        # Show the main welcome screen
        self.welcome_screen()

        # Start the GUI loop
        self.root.mainloop()

    # This creates a fancy dropdown menu with a colored style
    def create_custom_dropdown(self, var, options):
        dropdown = tk.OptionMenu(self.root, var, *options, command=lambda val: var.set(f"⮟ {val}"))
        dropdown.config(bg="#FBF0B1", fg="#E83455", font=("Century", 14, "bold"),
                        activebackground="#FBF0B1", activeforeground="#E83455", indicatoron=False)
        dropdown["menu"].config(bg="#FBF0B1", fg="#E83455", font=("Century", 12))
        return dropdown

    # This is the first screen that shows when the app opens
    def welcome_screen(self):
        # Show the main title
        self.canvas.create_text(375, 50, text="Decision Tree Classifier using Methods",
                                font=("Century", 26, "underline"), fill="#E83455")
        # Show instructions
        self.canvas.create_text(375, 100, text="Select two different attribute splitting methods:",
                                font=("Century", 18, "bold"), fill="#E83455")

        # Labels for method selection
        self.canvas.create_text(200, 170, text="Method 1 →", font=("Century", 24, "bold"), fill="#E83455")
        self.canvas.create_text(200, 230, text="Method 2 →", font=("Century", 24, "bold"), fill="#E83455")

        # Add the dropdowns
        dropdown1 = self.create_custom_dropdown(self.method_var1, list(self.METHODS.keys()))
        dropdown2 = self.create_custom_dropdown(self.method_var2, list(self.METHODS.keys()))
        self.canvas.create_window(500, 170, window=dropdown1)
        self.canvas.create_window(500, 230, window=dropdown2)

        # Button to run the decision tree comparison
        run_button = tk.Button(self.root, text="Run Decision Tree", font=("Century", 20, "bold"),
                               fg="#E83455", bg="#FBF0B1", width=25, command=self.run_selected_methods)
        self.canvas.create_window(375, 300, window=run_button)

        # Button to show all 5 methods together
        self.canvas.create_text(220, 700, text="View All Decision Tree Outcomes →",
                                font=("Century", 18), fill="#E83455")
        all_button = tk.Button(self.root, text="Show All Methods", font=("Century", 12, "bold"),
                               fg="#E83455", bg="#FBF0B1", command=self.show_all_methods)
        self.canvas.create_window(570, 700, window=all_button)

        # Footer text with your name and course
        self.canvas.create_text(375, 730, text="Sahad Rafiuzzaman | CS 580 | Assignment 4",
                                font=("Century", 16, "bold"), fill="#E83455")

    # This runs when the user selects two methods and clicks the Run button
    def run_selected_methods(self):
        method1 = self.method_var1.get().replace("⮟ ", "")
        method2 = self.method_var2.get().replace("⮟ ", "")

        # Make sure the user picked two different methods
        if method1 == method2:
            messagebox.showerror("Error", "Please select two different methods.")
            return
        if method1 not in self.METHODS or method2 not in self.METHODS:
            messagebox.showerror("Error", "Please select both methods.")
            return

        # Build trees using the two methods
        tree1 = self.METHODS[method1](train_data, attributes.copy())
        tree2 = self.METHODS[method2](train_data, attributes.copy())

        # Get the decision tree and prediction results as text
        output1 = f"--- {method1} Decision Tree ---\n" + "\n".join(print_tree(tree1))
        output1 += "\n\n--- Predictions ---\n" + evaluate(tree1, test_data)

        output2 = f"--- {method2} Decision Tree ---\n" + "\n".join(print_tree(tree2))
        output2 += "\n\n--- Predictions ---\n" + evaluate(tree2, test_data)

        # Show the result screen with both outputs
        self.display_result_screen(method1, output1, method2, output2)

    # This opens a new window to show two decision tree results side-by-side
    def display_result_screen(self, method1, text1, method2, text2):
        result_window = tk.Toplevel(self.root)
        result_window.title("Decision Tree Comparison")
        result_window.geometry("1200x600")

        container = tk.Frame(result_window)
        container.pack(fill="both", expand=True)

        # Left side (first method)
        frame1 = tk.Frame(container)
        frame1.pack(side="left", fill="both", expand=True, padx=10)
        tk.Label(frame1, text=method1, font=("Century", 16, "bold"), fg="#E83455").pack()
        text_area1 = scrolledtext.ScrolledText(frame1, wrap=tk.WORD, width=60, height=30)
        text_area1.insert(tk.END, text1)
        text_area1.pack()

        # Right side (second method)
        frame2 = tk.Frame(container)
        frame2.pack(side="right", fill="both", expand=True, padx=10)
        tk.Label(frame2, text=method2, font=("Century", 16, "bold"), fg="#E83455").pack()
        text_area2 = scrolledtext.ScrolledText(frame2, wrap=tk.WORD, width=60, height=30)
        text_area2.insert(tk.END, text2)
        text_area2.pack()

        # Button to close the result window
        back_button = tk.Button(result_window, text="Back to Welcome", command=result_window.destroy,
                                font=("Century", 12, "bold"), fg="#E83455", bg="#FBF0B1")
        back_button.pack(pady=5)

    # This opens a new window showing results for all five methods side-by-side
    def show_all_methods(self):
        from tkinter import Toplevel, Label, scrolledtext

        methods = {
            "Random": build_tree_random,
            "Least-Values": build_tree_least,
            "Most-Values": build_tree_most,
            "Gini Index": build_tree_gini,
            "Information Gain": build_tree_info_gain
        }

        result_window = Toplevel(self.root)
        result_window.title("All Method Combinations")
        result_window.geometry("1800x700")

        container = tk.Frame(result_window)
        container.pack(fill="both", expand=True)

        # For each method, build its tree and show the results
        for method_name, build_func in methods.items():
            tree = build_func(train_data, attributes.copy())
            output = f"--- {method_name} Decision Tree ---\n"
            output += "\n".join(print_tree(tree))
            output += "\n\n--- Predictions ---\n"
            output += evaluate(tree, test_data)

            method_frame = tk.Frame(container)
            method_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)

            Label(method_frame, text=method_name, font=("Century", 14, "bold"), fg="#E83455").pack()
            text_area = scrolledtext.ScrolledText(method_frame, wrap=tk.WORD, width=35, height=35)
            text_area.insert(tk.END, output)
            text_area.pack()

        # Back button to return to the welcome screen
        back_button = tk.Button(result_window, text="Back to Welcome", command=result_window.destroy,
                                font=("Century", 12, "bold"), fg="#E83455", bg="#FBF0B1")
        back_button.pack(pady=5)


# ---------- Run the GUI ---------- #
DecisionTreeGUI()

