# Homework Assignment 4: Decision Tree Classifier using Methods
CS 580: Introduction to Artificial Intelligence  
Author: Sahad Rafiuzzaman  
Date: 04/24/2025

## Overview
This project implements a Decision Tree Classifier from scratch for CS580 Introduction to Artificial Intelligence.
The program allows users to train and test decision trees using any two of the following five methods:
1. Random
2. Least-Values
3. Most-Values
4. Gini Index
5. Information Gain

It also includes a graphical user interface (GUI) built with Tkinter where users can:
1. Select two methods
2. View decision trees side by side
3. Compare predictions and accuracy
4. View results for all five methods together

No machine learning libraries like scikit-learn were used. The entire tree logic was written manually in Python. 

## Features
- Builds decision trees using 5 different splitting methods.
- Uses two CSV files for training and testing.
- GUI shows decision trees and predictions.
- Lets you compare any two methods side by side.
- Lets you view all five methods at once.

## Installation
Be sure to have Python installed along with the following libraries:
- tkinter - GUI framework for Python
- pandas
- math
- random
- PIL (Pillow)

### Install Dependencies
The following packages must be installed manually: Pillow
- To install the Pillow package, run the following:  
```pip install PIL``

## How to Run
1. Install the dependencies.
2. Place the following files in the same folder:
   - main.py
   - trainData.csv
   - testData.csv 
   - Decision_Tree_Image.jpg
3. Open a terminal or command prompt.
4. Run the program:
```python main.py```

## How it Works
1. Training: The selected decision tree methods use the training data to build trees.
2. Testing: The built trees are tested on the test data.
3. Evaluation: The model shows prediction accuracy and steps in the terminal.
4. GUI: Results and predictions are shown side by side in a Tkinter window.

## File Structure
1. main.py: The main Python script that includes all logic and the GUI. 
2. trainData.csv: Training data used to build the decision trees.
3. testData.csv: Test data used to evaluate prediction accuracy.
4. Decision_Tree_Image.jpg: Background image for the GUI.
5. README.md: This file.

## Acknowledgments
This project was developed with the help of various resources:
- https://stockcake.com/i/colorful-decision-tree_578600_1040538
- https://www.youtube.com/watch?v=WurCpmHtQc4&ab_channel=Codemy.com
- https://www.bogotobogo.com/python/scikit-learn/scikt_machine_learning_Decision_Tree_Learning_Informatioin_Gain_IG_Impurity_Entropy_Gini_Classification_Error.php

